import inspect

from django.forms import fields as django_fields

from .. import fields as extensible_fields
from ..fields import ExtensibleFieldMixin, datalist_field
from .boundfield import Bootstrap5BoundField

__all__ = (
	"Bootstrap5FieldMixin",
	"Bootstrap5MultiFieldMixin",
	"bootstrap5_field",
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
	if not issubclass(getattr(field, "bf_class", object), Bootstrap5BoundField):
		field = extensible_fields._monkey_patch_field(field, **kwargs)
		field.bf_class = kwargs.get("bf_class", Bootstrap5BoundField)
		if (
			getattr(field.widget, "input_type", None) == "checkbox"
			and "template_name" not in kwargs
		):
			field.label_suffix = ""
			field.template_name = (
				"django_extensible_forms/bootstrap5_forms/boolean_field.html"
			)
	return field


class Bootstrap5FieldMixin(ExtensibleFieldMixin):
	bf_class = Bootstrap5BoundField


class Bootstrap5MultiFieldMixin(Bootstrap5FieldMixin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for f in self.fields:
			_monkey_patch_field(f)


def bootstrap5_field(original_class):
	# create a new class prior to modifying it, so we don't
	# permanently change the original class
	assert inspect.isclass(
		original_class
	), f"You must pass the {original_class.__name__} class, not an instance of it."
	if issubclass(
		original_class, (django_fields.ComboField, django_fields.MultiValueField)
	):
		klass = Bootstrap5MultiFieldMixin
	else:
		klass = Bootstrap5FieldMixin
	return type(
		f"Bootstrap5{original_class.__name__}",
		(
			klass,
			original_class,
		),
		{},
	)


class CharField(Bootstrap5FieldMixin, extensible_fields.CharField):
	pass


class IntegerField(Bootstrap5FieldMixin, extensible_fields.IntegerField):
	pass


class FloatField(Bootstrap5FieldMixin, extensible_fields.FloatField):
	pass


class DecimalField(Bootstrap5FieldMixin, extensible_fields.DecimalField):
	pass


class BaseTemporalField(Bootstrap5FieldMixin, extensible_fields.BaseTemporalField):
	pass


class DateField(Bootstrap5FieldMixin, extensible_fields.DateField):
	pass


class TimeField(Bootstrap5FieldMixin, extensible_fields.TimeField):
	pass


class DateTimeField(Bootstrap5FieldMixin, extensible_fields.DateTimeField):
	pass


class DurationField(Bootstrap5FieldMixin, extensible_fields.DurationField):
	pass


class RegexField(Bootstrap5FieldMixin, extensible_fields.RegexField):
	pass


class EmailField(Bootstrap5FieldMixin, extensible_fields.EmailField):
	pass


class FileField(Bootstrap5FieldMixin, extensible_fields.FileField):
	pass


class ImageField(Bootstrap5FieldMixin, extensible_fields.ImageField):
	pass


class URLField(Bootstrap5FieldMixin, extensible_fields.URLField):
	pass


class BooleanField(Bootstrap5FieldMixin, extensible_fields.BooleanField):
	template_name = "django_extensible_forms/bootstrap5_forms/boolean_field.html"

	def __init__(self, *args, label_suffix="", **kwargs):
		super().__init__(*args, label_suffix=label_suffix, **kwargs)


class NullBooleanField(Bootstrap5FieldMixin, extensible_fields.NullBooleanField):
	pass


class ChoiceField(Bootstrap5FieldMixin, extensible_fields.ChoiceField):
	pass


class TypedChoiceField(Bootstrap5FieldMixin, extensible_fields.TypedChoiceField):
	pass


class MultipleChoiceField(Bootstrap5FieldMixin, extensible_fields.MultipleChoiceField):
	pass


class TypedMultipleChoiceField(
	Bootstrap5FieldMixin, extensible_fields.TypedMultipleChoiceField
):
	pass


class ComboField(Bootstrap5MultiFieldMixin, django_fields.ComboField):
	pass


class MultiValueField(Bootstrap5MultiFieldMixin, django_fields.MultiValueField):
	pass


class FilePathField(Bootstrap5FieldMixin, extensible_fields.FilePathField):
	pass


class SplitDateTimeField(Bootstrap5MultiFieldMixin, django_fields.SplitDateTimeField):
	pass


class GenericIPAddressField(
	Bootstrap5FieldMixin, extensible_fields.GenericIPAddressField
):
	pass


class SlugField(Bootstrap5FieldMixin, extensible_fields.SlugField):
	pass


class UUIDField(Bootstrap5FieldMixin, extensible_fields.UUIDField):
	pass


class JSONField(Bootstrap5FieldMixin, extensible_fields.JSONField):
	pass


class RangeField(Bootstrap5FieldMixin, extensible_fields.RangeField):
	pass


class UsernameField(Bootstrap5FieldMixin, extensible_fields.UsernameField):
	pass
