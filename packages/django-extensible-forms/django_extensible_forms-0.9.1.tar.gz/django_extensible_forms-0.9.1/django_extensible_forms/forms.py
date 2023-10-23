import copy
import inspect

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from django.forms.models import ALL_FIELDS
from django.forms.utils import RenderableErrorMixin
from django.utils.translation import gettext_lazy as _

from .boundfield import ExtensibleBoundField
from .fields import _monkey_patch_field
from .utils import (
	FieldErrorDict,
	FieldErrorList,
	FieldErrorMixin,
	configure_form_attrs,
	configure_form_css,
	configure_form_localization,
)

__all__ = (
	"extensible_form",
	"FieldErrorMixin",
	"FieldErrorList",
	"FieldErrorDict",
	"ExtensibleFormOptions",
	"ExtensibleFormMetaclass",
	"BaseExtensibleForm",
	"Form",
)


def extensible_form(form_class):
	assert inspect.isclass(
		form_class
	), f"You must pass the {form_class.__name__} class, not an instance of it."
	return type(f"Extensible{form_class.__name__}", (form_class, Form), {})


class ExtensibleFormOptions:
	attrs = (
		"template_name",
		"template_name_label",
		"css",
		"attrs",
		"help_texts",
		"error_class",
		"field_error_class",
		"localized_fields",
		"field_order",
	)

	def __init__(self, options=None):
		for attr in dir(options):
			assert attr in self.attrs or attr.startswith(
				"__"
			), f"Unknown attribute '{attr}' specified in form Meta."
		self.template_name = getattr(options, "template_name", None)
		self.template_name_label = getattr(options, "template_name_label", None)
		self.css = getattr(options, "css", None)
		self.attrs = getattr(options, "attrs", None)
		self.help_texts = getattr(options, "help_texts", None)
		self.error_class = getattr(options, "error_class", None)
		self.field_error_class = getattr(options, "field_error_class", None)
		self.localized_fields = getattr(options, "localized_fields", None)
		self.field_order = getattr(options, "field_order", None)


class ExtensibleFormMetaclass(DeclarativeFieldsMetaclass):
	def __new__(mcs, name, bases, attrs):
		new_class = super().__new__(mcs, name, bases, attrs)
		if mcs.bases_check(mcs, bases):
			return new_class
		meta = new_class._meta = mcs.get_meta_opts_class()(
			getattr(new_class, "Meta", None)
		)
		# set new class attributes
		mcs.construct_class(mcs, meta, new_class)
		# ensure all fields are extensibles
		mcs.ensure_extensified_fields(mcs, new_class)
		# set localization on fields
		mcs.configure_field_localization(mcs, meta, new_class)
		# check error classes
		mcs.configure_error_classes(mcs, meta, new_class)
		# attrs specifications
		mcs.configure_attrs(mcs, meta, new_class)
		# css specifications
		mcs.configure_css(mcs, meta, new_class)
		# help text specifications
		mcs.configure_help_texts(mcs, meta, new_class)
		return new_class

	def bases_check(mcs, bases):
		return bases == (BaseExtensibleForm,)

	def get_meta_opts_class():
		return ExtensibleFormOptions

	def ensure_extensified_fields(mcs, new_class):
		for field_name, field in new_class.base_fields.items():
			if not issubclass(getattr(field, "bf_class", object), ExtensibleBoundField):
				new_class.base_fields[field_name] = _monkey_patch_field(field)

	def construct_class(mcs, meta, new_class):
		# set attributes from metaclass for new instance
		if meta.template_name and 'template_name' not in vars(new_class):
			new_class.template_name = meta.template_name
		if meta.template_name_label and 'template_name_label' not in vars(new_class):
			new_class.template_name_label = meta.template_name_label
		if meta.field_order:
			new_class.field_order = meta.field_order
		# deep copy base fields so we don't change parent classes' base fields
		# when we apply our Meta modifications
		new_class.declared_fields = copy.deepcopy(new_class.declared_fields)
		new_class.base_fields = new_class.declared_fields

	def configure_field_localization(mcs, meta, new_class):
		if meta.localized_fields is not None:
			assert meta.localized_fields == ALL_FIELDS or hasattr(
				meta.localized_fields, "__next__"
			), (
				"%(form)s.Meta.localized_fields must be an iterable or '%(all_fields)s'."
				% {"form": new_class.__name__, "all_fields": ALL_FIELDS}
			)
			if meta.localized_fields == ALL_FIELDS:
				for field in new_class.base_fields.values():
					field.localize = True
			elif not isinstance(meta.localized_fields, str) and hasattr(
				meta.localized_fields, "__next__"
			):
				for field in meta.localized_fields:
					try:
						new_class.base_fields[field].localize = True
					except KeyError as e:
						raise e(
							"%(field)s is not a field of %(form)s, but it is specified"
							"in %(form)s.Meta.localized_fields. Is this a typo?"
							% {"field": field, "form": new_class.__name__}
						)
			else:
				raise TypeError(
					"%(form)s.Meta.localized_fields must be an iterable or '%(all_fields)s'."
					% {"form": new_class.__name__, "all_fields": ALL_FIELDS}
				)

	def configure_error_classes(mcs, meta, new_class):
		for opt in ["field_error_class", "error_class"]:
			error_class = getattr(meta, opt)
			if error_class:
				error_class_type = (
					RenderableErrorMixin
					if not opt == "field_error_class"
					else FieldErrorMixin
				)
				if issubclass(error_class, error_class_type):
					setattr(new_class, opt, error_class)
				else:
					raise TypeError(
						"%(form)s.Meta.%(opt)s must be a subclass of either %(error_class)s."
						% {
							"form": new_class.__name__,
							"opt": opt,
							"error_class": error_class_type.__name__,
						}
					)

	def configure_attrs(mcs, meta, new_class):
		PERMISSIBLE_PROPS = {"fields", "labels", "help_texts"}
		# skip if not defined
		if meta.attrs is None:
			return
		# coerce type
		try:
			meta.attrs = dict(meta.attrs)
		except (ValueError, TypeError):
			raise TypeError(
				"%(form)s.Meta.attrs must castable to a dict."
				% {"form": new_class.__name__}
			)
		# check attrs structure
		for prop, value in meta.attrs.items():
			assert (
				prop in PERMISSIBLE_PROPS
			), "%(form)s.Meta.attrs['%(property)s'] is not an accepted property." % {
				"form": new_class.__name__,
				"property": prop,
			}
			# skip if intentionally set None
			if value is None:
				continue
			# coerce attrs to proper type
			try:
				meta.attrs[prop] = dict(value)
			except (ValueError, TypeError):
				raise TypeError(
					"%(form)s.Meta.attrs['%(property)s'] must castable to `dict`."
					% {"form": new_class.__name__, "property": prop}
				)
		# now try to apply it
		try:
			# define an attr Meta to field attribute pair
			pairs = (
				("fields", "attrs"),
				("labels", "label_attrs"),
				("help_texts", "help_text_attrs"),
			)
			# apply attrs to each field, where present
			for field_name, field in new_class.base_fields.items():
				for key, attr in pairs:
					attrs = {}
					# skip if not defined
					if key not in meta.attrs:
						continue
					# add global attrs, if any
					if ALL_FIELDS in meta.attrs[key]:
						attrs |= dict(meta.attrs[key][ALL_FIELDS])
					# add field specific attrs
					if field_name in meta.attrs[key]:
						attrs |= dict(meta.attrs[key][field_name])
					# preference field attr definitions over meta attr definitions
					field_attrs = getattr(field, attr, None)
					if field_attrs:
						attrs |= field_attrs
					# apply collected attrs
					if attrs:
						setattr(field, attr, attrs)
		except (ValueError, TypeError):
			raise TypeError(
				"%(form)s.Meta.attrs is misconfigured." % {"form": new_class.__name__}
			)

	def configure_css(mcs, meta, new_class):
		PERMISSIBLE_PROPS = {
			"form",
			"fields",
			"labels",
			"field_errors",
			"separators",
			"help_texts",
		}
		# skip if not defined
		if meta.css is None:
			return
		# coerce type
		try:
			meta.css = dict(meta.css)
		except (ValueError, TypeError):
			raise TypeError(
				"%(form)s.Meta.css must castable to a dict."
				% {"form": new_class.__name__}
			)
		# check css structure
		for prop, value in meta.css.items():
			assert (
				prop in PERMISSIBLE_PROPS
			), "%(form)s.Meta.css['%(property)s'] is not an accepted property." % {
				"form": new_class.__name__,
				"property": prop,
			}
			if not isinstance(meta.css[prop], str):
				# coerce field-level css attributes into dict
				try:
					meta.css[prop] = dict(value)
				except (ValueError, TypeError):
					raise TypeError(
						"%(form)s.Meta.css['%(property)s'] must castable to a dict."
						% {"form": new_class.__name__, "property": prop}
					)
		# now try to apply it
		try:
			# set form css classes
			if "form" in meta.css:
				pairs = (
					("error_field", "error_css_class"),
					("required_field", "required_css_class"),
					("non_field_errors", "non_field_errors_css_class"),
				)
				for key, attr in pairs:
					if not hasattr(new_class, attr) and key in meta.css["form"]:
						setattr(new_class, attr, meta.css["form"][key])
			# define a css Meta to field attribute pair
			pairs = (
				("fields", "css"),
				("labels", "label_css"),
				("field_errors", "error_css"),
				("separators", "separator_css"),
				("help_texts", "help_text_css"),
			)
			# apply css classes to each field, where present
			for field_name, field in new_class.base_fields.items():
				for key, attr in pairs:
					css_classes = set()
					# skip if overridden
					if getattr(field, attr, None):
						continue
					# skip if not defined
					if key not in meta.css:
						continue
					if isinstance(meta.css[key], dict):
						# add global css, if any
						if ALL_FIELDS in meta.css[key]:
							css_classes |= set(
								list(
									meta.css[key][ALL_FIELDS].split()
									if hasattr(meta.css[key][ALL_FIELDS], "split")
									else meta.css[key][ALL_FIELDS]
								)
							)
						# add field specific css
						if field_name in meta.css[key]:
							css_classes |= set(
								list(
									meta.css[key][field_name].split()
									if hasattr(meta.css[key][field_name], "split")
									else meta.css[key][field_name]
								)
							)
					elif isinstance(meta.css[key], str):
						css_classes = set(meta.css[key].split())
					# apply collected css classes
					if css_classes:
						setattr(field, attr, css_classes)
		except (ValueError, TypeError):
			raise TypeError(
				"%(form)s.Meta.css is misconfigured." % {"form": new_class.__name__}
			)

	def configure_help_texts(mcs, meta, new_class):
		# skip if not defined
		if meta.help_texts is None:
			return
		# coerce type
		try:
			meta.help_texts = dict(meta.help_texts)
		except (ValueError, TypeError):
			raise TypeError(
				"%(form)s.Meta.help_texts must castable to a dict."
				% {"form": new_class.__name__}
			)
		# apply attrs to each field, where present
		for field_name, field in new_class.base_fields.items():
			# skip if overridden
			if getattr(field, "help_text", None):
				continue
			# add field specific attrs
			if field_name in meta.help_texts:
				help_text = meta.help_texts[field_name]
				setattr(field, "help_text", help_text)


class ExtensibleFormMixin:
	field_error_class = FieldErrorList

	required_css_class = "required"
	field_error_css_class = "invalid"
	field_help_text_css_class = "helptext"
	non_field_errors_css_class = "nonfield"

	template_name_div = "django_extensible_forms/forms/div.html"
	template_name_p = "django_extensible_forms/forms/p.html"
	template_name_table = "django_extensible_forms/forms/table.html"
	template_name_ul = "django_extensible_forms/forms/ul.html"
	template_name_label = "django/forms/label.html"

	def __init__(
		self,
		*args,
		id: str = None,
		css: dict = None,
		attrs: dict = None,
		localized_fields: list | tuple | str = None,
		field_error_class: FieldErrorMixin = None,
		template_name: str = None,
		**kwargs,
	):
		super().__init__(*args, **kwargs)
		self.html_id = id or type(self).__name__
		meta = getattr(self, "_meta", None)
		self.field_error_class = (
			field_error_class
			or getattr(meta, "field_error_class", None)
			or self.field_error_class
		)
		# work-around due to the way django checks label css attribute for required fields
		if hasattr(self, "required_css_class") and not self.required_css_class:
			self.required_css_class = ""
		# adjust form based on init args
		if css:
			configure_form_css(self, css)
		if attrs:
			configure_form_attrs(self, attrs)
		if localized_fields:
			configure_form_localization(self, localized_fields)
		if template_name:
			self.template_name = template_name

	@property
	def template_name(self):
		if hasattr(self, '_template_name'):
			return self._template_name
		return self.renderer.form_template_name
	
	@template_name.setter
	def template_name(self, value):
		self._template_name = value

	# identitical to django implementation except bf is passed to self.field_error_class
	def get_context(self):
		fields = []
		hidden_fields = []
		top_errors = self.non_field_errors().copy()
		for name, bf in self._bound_items():
			# new error class expects the bound field to be passed to it
			bf_errors = self.field_error_class(
				bf.errors, boundfield=bf, renderer=self.renderer
			)
			if bf.is_hidden:
				if bf_errors:
					top_errors += [
						_("(Hidden field %(name)s) %(error)s")
						% {"name": name, "error": str(e)}
						for e in bf_errors
					]
				hidden_fields.append(bf)
			else:
				errors_str = str(bf_errors)
				fields.append((bf, errors_str))
		return {
			"form": self,
			"fields": fields,
			"hidden_fields": hidden_fields,
			"errors": top_errors,
		}

	# identitical to django implementation except uses self.field_error_class for
	# field errors and self.non_field_errors_css_class for non field error css
	def add_error(self, field, error):
		if not isinstance(error, ValidationError):
			# Normalize to ValidationError and let its constructor
			# do the hard work of making sense of the input.
			error = ValidationError(error)

		if hasattr(error, "error_dict"):
			if field is not None:
				raise TypeError(
					"The argument `field` must be `None` when the `error` "
					"argument contains errors for multiple fields."
				)
			else:
				error = error.error_dict
		else:
			error = {field or NON_FIELD_ERRORS: error.error_list}

		for field, error_list in error.items():
			if field not in self.errors:
				if field != NON_FIELD_ERRORS and field not in self.fields:
					raise ValueError(
						"'%s' has no field named '%s'."
						% (self.__class__.__name__, field)
					)
				if field == NON_FIELD_ERRORS:
					self._errors[field] = self.error_class(
						error_class=self.non_field_errors_css_class,
						renderer=self.renderer,
					)
				else:
					self._errors[field] = self.field_error_class(
						boundfield=self[field], renderer=self.renderer
					)
			self._errors[field].extend(error_list)
			if field in self.cleaned_data:
				del self.cleaned_data[field]

	# identitical to django implementation except the errors css is configurable via Meta
	def non_field_errors(self):
		return self.errors.get(
			NON_FIELD_ERRORS,
			self.error_class(
				error_class=self.non_field_errors_css_class, renderer=self.renderer
			),
		)


class BaseExtensibleForm(ExtensibleFormMixin, BaseForm):
	pass


class Form(BaseExtensibleForm, metaclass=ExtensibleFormMetaclass):
	pass
