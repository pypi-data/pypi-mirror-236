import inspect

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import OperationalError
from django.forms import fields as django_fields
from django.forms.boundfield import BoundField
from django.utils.translation import gettext_lazy as _

from .boundfield import ExtensibleBoundField
from .mutators import DatalistWidgetMutator
from .widgets import RangeInput

__all__ = (
	"ExtensibleFieldMixin",
	"ExtensibleMultiFieldMixin",
	"DatalistFieldMixin",
	"extensible_field",
	"datalist_field",
	"CharField",
	"IntegerField",
	"DateField",
	"TimeField",
	"DateTimeField",
	"DurationField",
	"RegexField",
	"EmailField",
	"FileField",
	"ImageField",
	"URLField",
	"BooleanField",
	"NullBooleanField",
	"ChoiceField",
	"MultipleChoiceField",
	"ComboField",
	"MultiValueField",
	"FloatField",
	"DecimalField",
	"SplitDateTimeField",
	"GenericIPAddressField",
	"FilePathField",
	"JSONField",
	"SlugField",
	"TypedChoiceField",
	"TypedMultipleChoiceField",
	"UUIDField",
	"RangeField",
	"UsernameField",
)


def _monkey_patch_field(field, **kwargs):
	if isinstance(field, (django_fields.ComboField, django_fields.MultiValueField)):
		for f in field.fields:
			_monkey_patch_field(f, **kwargs)
	if not issubclass(getattr(field, "bf_class", object), ExtensibleBoundField):
		# set default attributes
		field.readonly = getattr(field, "readonly", kwargs.get("readonly", False))
		field.css = getattr(field, "css", kwargs.get("css"))
		field.label_css = getattr(field, "label_css", kwargs.get("label_css"))
		field.error_css = getattr(field, "error_css", kwargs.get("error_css"))
		field.separator_css = getattr(
			field, "separator_css", kwargs.get("separator_css")
		)
		field.help_text_css = getattr(
			field, "help_text_css", kwargs.get("help_text_css", "helptext")
		)
		field.attrs = getattr(field, "attrs", kwargs.get("attrs"))
		field.label_attrs = getattr(field, "label_attrs", kwargs.get("label_attrs"))
		field.separator_attrs = getattr(
			field, "separator_attrs", kwargs.get("separator_attrs")
		)
		field.help_text_attrs = getattr(
			field, "help_text_attrs", kwargs.get("help_text_attrs")
		)
		field.bf_class = kwargs.get("bf_class", ExtensibleBoundField)
		field.template_name = kwargs.get(
			"template_name", "django_extensible_forms/forms/field.html"
		)
		# override get_bound_field()
		method = ExtensibleFieldMixin.get_bound_field
		setattr(type(field), "get_bound_field", method)
		# OLD METHOD BELOW
		# this does not work! `field` is always the form.base_field['field_name'] instance,
		# NOT the real field attached to the form instance at form.fields['field_name']
		# field.get_bound_field = method.__get__(field, type(field))
	return field


class ExtensibleFieldMixin:
	css = None
	label_css = None
	error_css = None
	separator_css = None
	help_text_css = None
	attrs: dict = None
	label_attrs: dict = None
	separator_attrs: dict = None
	help_text_attrs: dict = None
	bf_class = ExtensibleBoundField
	template_name = "django_extensible_forms/forms/field.html"

	def __init__(
		self,
		*args,
		readonly=False,
		css=None,
		label_css=None,
		error_css=None,
		separator_css=None,
		help_text_css=None,
		attrs=None,
		label_attrs=None,
		separator_attrs=None,
		help_text_attrs=None,
		bf_class=None,
		**kwargs,
	):
		# get all argspecs of parent __init__() methods
		argspecs = [
			inspect.getfullargspec(klass.__init__)
			for klass in type(self).__mro__
			if hasattr(klass.__init__, "__name__")
			and klass.__init__.__name__ == "__init__"
		]
		# get all keyword-only args and required args of parent __init__() methods
		kws = []
		for argspec in argspecs:
			kws.extend(argspec.kwonlyargs)
			kws.extend(argspec.args[: len(argspec.args) - len(argspec.defaults or [])])
		# filter out kwargs intended for the modified __init__()
		orig_kwargs = {key: kwargs.pop(key) for key in kws if key in kwargs}
		# call original __init__
		super().__init__(*args, **orig_kwargs)
		# the HTML form read-only attribute
		self.readonly = readonly
		# add css
		try:
			for attr, css_classes in (
				("css", css),
				("label_css", label_css),
				("error_css", error_css),
				("separator_css", separator_css),
				("help_text_css", help_text_css),
			):
				if css_classes:
					if hasattr(css_classes, "split"):
						css_classes = css_classes.split()
					setattr(self, attr, set(css_classes))
				else:
					setattr(self, attr, getattr(self, attr, None))
		except (ValueError, TypeError):
			raise TypeError(
				"%(attr)s must be an iterable or a string when instantiating %(class)s"
				% {"attr": attr, "class": type(self).__name__}
			)
		# add attrs
		try:
			for attr, value in (
				("attrs", attrs),
				("label_attrs", label_attrs),
				("separator_attrs", separator_attrs),
				("help_text_attrs", help_text_attrs),
			):
				if value:
					setattr(self, attr, dict(value))
				else:
					setattr(self, attr, getattr(self, attr, None))
		except (ValueError, TypeError):
			raise TypeError(
				"%(attr)s must be a dict when instantiating %(class)s"
				% {"attr": attr, "class": type(self).__name__}
			)
		# add any additional kwargs as HTML attributes
		extra_attrs = {
			key: value for key, value in kwargs.items() if key not in orig_kwargs
		}
		if extra_attrs:
			if self.attrs:
				self.attrs |= extra_attrs
			else:
				self.attrs = extra_attrs
		# define the boundfield class to use
		if bf_class:
			self.bf_class = bf_class

	def get_bound_field(self, form, field_name):
		"""
		Modified to return self.bf_class instead
		of always django's BoundField class.
		"""
		if not hasattr(self, "bf_class"):
			return BoundField(form, self, field_name)
		return self.bf_class(form, self, field_name)


class ExtensibleMultiFieldMixin(ExtensibleFieldMixin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for f in self.fields:
			_monkey_patch_field(f)


class DatalistFieldMixin(ExtensibleFieldMixin):
	def __init__(self, *args, datalist=None, **kwargs):
		super().__init__(*args, **kwargs)
		if datalist:
			if not hasattr(datalist, "__iter__"):
				raise TypeError(
					"%(class)s datalist must be an iterable, not a %(type)s."
					% {"class": self.__class__.__name__, "type": type(datalist)}
				)
			mutator = DatalistWidgetMutator()
			self.widget = mutator(self.widget, datalist=datalist)


def extensible_field(original_class):
	# create a new class prior to modifying it, so we don't
	# permanently change the original class
	assert inspect.isclass(
		original_class
	), f"You must pass the {original_class.__name__} class, not an instance of it."
	if issubclass(
		original_class, (django_fields.ComboField, django_fields.MultiValueField)
	):
		klass = ExtensibleMultiFieldMixin
	else:
		klass = ExtensibleFieldMixin
	return type(
		f"Extensible{original_class.__name__}",
		(
			klass,
			original_class,
		),
		{},
	)


def datalist_field(original_class):
	assert inspect.isclass(original_class), (
		f"You must pass the {original_class.__name__} class, " f"not an instance of it."
	)
	return type(
		f"Datalist{original_class.__name__}",
		(
			DatalistFieldMixin,
			original_class,
		),
		{},
	)


class CharField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.CharField):
	pass


class IntegerField(
	DatalistFieldMixin, ExtensibleFieldMixin, django_fields.IntegerField
):
	pass


class FloatField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.FloatField):
	pass


class DecimalField(
	DatalistFieldMixin, ExtensibleFieldMixin, django_fields.DecimalField
):
	pass


class BaseTemporalField(
	DatalistFieldMixin, ExtensibleFieldMixin, django_fields.BaseTemporalField
):
	pass


class DateField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.DateField):
	pass


class TimeField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.TimeField):
	pass


class DateTimeField(
	DatalistFieldMixin, ExtensibleFieldMixin, django_fields.DateTimeField
):
	pass


class DurationField(
	DatalistFieldMixin, ExtensibleFieldMixin, django_fields.DurationField
):
	pass


class RegexField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.RegexField):
	pass


class EmailField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.EmailField):
	pass


class FileField(ExtensibleFieldMixin, django_fields.FileField):
	pass


class ImageField(ExtensibleFieldMixin, django_fields.ImageField):
	pass


class URLField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.URLField):
	pass


class BooleanField(ExtensibleFieldMixin, django_fields.BooleanField):
	pass


class NullBooleanField(ExtensibleFieldMixin, django_fields.NullBooleanField):
	pass


class ChoiceField(ExtensibleFieldMixin, django_fields.ChoiceField):
	pass


class TypedChoiceField(ChoiceField, django_fields.TypedChoiceField):
	pass


class MultipleChoiceField(ChoiceField, django_fields.MultipleChoiceField):
	pass


class TypedMultipleChoiceField(
	ExtensibleFieldMixin, django_fields.TypedMultipleChoiceField
):
	pass


class ComboField(ExtensibleMultiFieldMixin, django_fields.ComboField):
	pass


class MultiValueField(ExtensibleMultiFieldMixin, django_fields.MultiValueField):
	pass


class FilePathField(ExtensibleFieldMixin, django_fields.FilePathField):
	pass


class SplitDateTimeField(ExtensibleMultiFieldMixin, django_fields.SplitDateTimeField):
	pass


class GenericIPAddressField(
	DatalistFieldMixin, ExtensibleFieldMixin, django_fields.GenericIPAddressField
):
	pass


class SlugField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.SlugField):
	pass


class UUIDField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.UUIDField):
	pass


class JSONField(DatalistFieldMixin, ExtensibleFieldMixin, django_fields.JSONField):
	pass


class RangeField(MultiValueField):
	widget = RangeInput

	def __init__(self, fields=None, *args, **kwargs):
		if fields is None:
			fields = (django_fields.DecimalField(), django_fields.DecimalField())
		super().__init__(fields, *args, **kwargs)

	def compress(self, data_list):
		if data_list:
			return {"lower": data_list[0], "upper": data_list[1]}


class UsernameField(CharField):
	"""A CharField which validates to a user object."""

	default_error_messages = {
		"invalid_username": _(
			"That user does not exist. Please enter a valid username."
		),
	}

	def __init__(self, *, queryset=None, datalist=None, **kwargs):
		self._model = self._get_model()
		self.queryset = self._get_queryset(queryset)
		# wrapped in try/except as this may cause an OperationalError if
		# db hasn't been migrated first
		try:
			datalist = (
				None
				if datalist is False
				else list(self.queryset.values_list("username", flat=True))
			)
		except OperationalError:
			datalist = None
		super().__init__(datalist=datalist, **kwargs)

	def _get_model(self):
		return getattr(self, "_model", get_user_model())

	def _get_queryset(self, queryset=None):
		if queryset:
			assert queryset.model is self._model, (
				"%(class)s queryset expects a Queryset of '%(model)s', not '%(incorrect)s'."
				% {
					"class": self.__class__,
					"model": self._model,
					"incorrect": queryset.model,
				}
			)
			return queryset
		return self._model.objects.filter(is_active=True)

	def __deepcopy__(self, memo):
		result = super().__deepcopy__(memo)
		result.queryset = (
			self.queryset.all() if self.queryset is not None else result.queryset
		)
		return result

	def to_python(self, value):
		if value in self.empty_values:
			return None
		try:
			if isinstance(value, self._model):
				value = getattr(value, "username")
			value = self.queryset.get(username__iexact=value)
		except (ValueError, TypeError, self._model.DoesNotExist):
			raise ValidationError(
				self.error_messages["invalid_username"],
				code="invalid_username",
				params={"value": value},
			)
		return value

	def prepare_value(self, value):
		try:
			return self._model.objects.get(username__iexact=value)
		except (ValueError, TypeError, self._model.DoesNotExist):
			return super().prepare_value(value)

	def has_changed(self, initial, data):
		initial = self.prepare_value(initial)
		return super().has_changed(initial, data)
