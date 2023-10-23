from django.forms.models import ALL_FIELDS
from django.forms.utils import ErrorDict, ErrorList, RenderableMixin

__all__ = ("FieldErrorList", "FieldErrorDict")


class RenderableFieldMixin(RenderableMixin):
	def as_field_group(self):
		return self.render()

	def as_hidden(self):
		raise NotImplementedError(
			"Subclasses of RenderableFieldMixin must provide an as_hidden() method."
		)

	def as_widget(self):
		raise NotImplementedError(
			"Subclasses of RenderableFieldMixin must provide an as_widget() method."
		)

	def __str__(self):
		"""Render this field as an HTML widget."""
		if self.field.show_hidden_initial:
			return self.as_widget() + self.as_hidden(only_initial=True)
		return self.as_widget()

	__html__ = __str__


class FieldErrorMixin:
	def __init__(self, *args, boundfield=None, **kwargs):
		super().__init__(*args, **kwargs)
		assert boundfield is not None, "`boundfield` must be specified"
		self.boundfield = boundfield

	def get_context(self):
		context = super().get_context()
		context["field"] = self.boundfield
		return context


class FieldErrorList(FieldErrorMixin, ErrorList):
	template_name = "django_extensible_forms/forms/errors/list/field_default.html"


class FieldErrorDict(FieldErrorMixin, ErrorDict):
	template_name = "django_extensible_forms/forms/errors/dict/field_default.html"


def configure_form_css(form, css: dict):
	PERMISSIBLE_PROPS = {
		"form",
		"fields",
		"labels",
		"field_errors",
		"separators",
		"help_texts",
	}
	# check css structure
	for prop, value in css.items():
		if prop not in PERMISSIBLE_PROPS:
			raise ValueError(
				"Invalid css passed to %(form)s: css['%(property)s'] is not an accepted property."
				% {
					"form": type(form).__name__,
					"property": prop,
				}
			)
		if not isinstance(css[prop], str):
			# coerce field-level css attributes into dict
			try:
				css[prop] = dict(value)
			except (ValueError, TypeError):
				raise TypeError(
					"Invalid css passed to %(form)s: css['%(property)s'] must castable to a dict."
					% {"form": type(form).__name__, "property": prop}
				)
	# now try to apply it
	try:
		# set form css classes
		if "form" in css:
			pairs = (
				("error_field", "error_css_class"),
				("required_field", "required_css_class"),
				("non_field_errors", "non_field_errors_css_class"),
			)
			for key, attr in pairs:
				if key in css["form"]:
					setattr(form, attr, css["form"][key])
		pairs = (
			("fields", "css"),
			("labels", "label_css"),
			("field_errors", "error_css"),
			("separators", "separator_css"),
			("help_texts", "help_text_css"),
		)
		# apply css classes to each field, where present
		for field_name, field in form.fields.items():
			for key, attr in pairs:
				css_classes = set()
				# skip if not defined
				if key not in css:
					continue
				if isinstance(css[key], dict):
					# add global css, if any
					if ALL_FIELDS in css[key]:
						css_classes |= set(
							list(
								css[key][ALL_FIELDS].split()
								if hasattr(css[key][ALL_FIELDS], "split")
								else css[key][ALL_FIELDS]
							)
						)
					# add field specific css
					if field_name in css[key]:
						css_classes |= set(
							list(
								css[key][field_name].split()
								if hasattr(css[key][field_name], "split")
								else css[key][field_name]
							)
						)
				elif isinstance(css[key], str):
					css_classes = set(css[key].split())
				# apply collected css classes
				if css_classes:
					setattr(field, attr, css_classes)
	except (ValueError, TypeError):
		raise TypeError(
			"Invalid css passed to %(form)s." % {"form": type(form).__name__}
		)


def configure_form_attrs(form, attrs: dict):
	PERMISSIBLE_PROPS = {"fields", "labels", "help_texts"}
	# check attrs structure
	for prop, value in attrs.items():
		if prop not in PERMISSIBLE_PROPS:
			raise ValueError(
				"Invalid attrs passed to %(form)s: attrs['%(property)s'] is not an accepted property."
				% {
					"form": type(form).__name__,
					"property": prop,
				}
			)
		# coerce attrs to proper type
		if value is not None:
			try:
				attrs[prop] = dict(value)
			except (ValueError, TypeError):
				raise TypeError(
					"Invalid attrs passed to %(form)s: attrs['%(property)s'] must castable to a dict."
					% {"form": type(form).__name__, "property": prop}
				)
	# now try to apply it
	try:
		pairs = (
			("fields", "attrs"),
			("labels", "label_attrs"),
			("help_texts", "help_text_attrs"),
		)
		# apply attrs to each field, where present
		for field_name, field in form.fields.items():
			for key, attr in pairs:
				field_attrs = {}
				# skip if not defined
				if key not in attrs:
					continue
				# add global attrs, if any
				if ALL_FIELDS in attrs[key]:
					field_attrs |= dict(attrs[key][ALL_FIELDS])
				# add field specific attrs
				if field_name in attrs[key]:
					field_attrs |= dict(attrs[key][field_name])
				# apply collected attrs
				if field_attrs:
					setattr(field, attr, field_attrs)
	except (ValueError, TypeError):
		raise TypeError(
			"Invalid attrs passed to %(form)s." % {"form": type(form).__name__}
		)


def configure_form_localization(form, fields: list | tuple | str):
	if fields == ALL_FIELDS:
		for field in form.fields.values():
			field.localize = True
	elif not isinstance(fields, str) and hasattr(fields, "__next__"):
		for field in fields:
			try:
				form.fields[field].localize = True
			except KeyError as e:
				raise e(
					"Invalid localized_fields passed to %(form)s: %(field)s does not correspond to a field in the form."
					% {
						"form": type(form).__name__,
						"field": field,
					}
				)
	else:
		raise TypeError(
			"Invalid localized_fields passed to %(form)s: must be an iterable or '%(all_fields)s'."
			% {"form": type(form).__name__, "all_fields": ALL_FIELDS}
		)
