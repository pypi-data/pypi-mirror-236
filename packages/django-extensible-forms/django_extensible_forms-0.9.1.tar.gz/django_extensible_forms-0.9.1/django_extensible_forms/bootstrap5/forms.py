import inspect

from django.forms.forms import BaseForm

from ..forms import ExtensibleFormMetaclass, ExtensibleFormMixin
from .boundfield import Bootstrap5BoundField
from .fields import _monkey_patch_field
from .utils import FieldErrorList

__all__ = (
	"bootstrap5_form",
	"Bootstrap5FormMetaclass",
	"BaseBootstrap5Form",
	"Form",
)


def bootstrap5_form(form_class):
	assert inspect.isclass(form_class), (
		f"You must pass the {form_class.__name__} class, " f"not an instance of it."
	)
	return type(f"Bootstrap5{form_class.__name__}", (form_class, Form), {})


class Bootstrap5FormMetaclass(ExtensibleFormMetaclass):
	def bases_check(mcs, bases):
		return bases == (BaseBootstrap5Form,)

	def ensure_extensified_fields(mcs, new_class):
		for field_name, field in new_class.base_fields.items():
			if not issubclass(getattr(field, "bf_class", object), Bootstrap5BoundField):
				new_class.base_fields[field_name] = _monkey_patch_field(field)


class Bootstrap5FormMixin(ExtensibleFormMixin):
	required_css_class = None
	field_error_css_class = "is-invalid"
	field_help_text_css_class = "form-text"
	field_error_class = FieldErrorList


class BaseBootstrap5Form(Bootstrap5FormMixin, BaseForm):
	pass


class Form(BaseBootstrap5Form, metaclass=Bootstrap5FormMetaclass):
	pass
