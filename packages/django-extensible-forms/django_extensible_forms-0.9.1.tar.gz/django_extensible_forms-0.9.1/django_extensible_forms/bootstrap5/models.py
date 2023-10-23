from ..models import (
	BaseExtensibleModelForm,
	ExtensibleModelFormMetaclass,
	ModelChoiceField as ExtensibleModelChoiceField,
	ModelMultipleChoiceField as ExtensibleModelMultipleChoiceField,
	extensible_formfield_callback,
	modelform_factory as extensible_modelform_factory,
)
from .fields import Bootstrap5FieldMixin, _monkey_patch_field
from .forms import Bootstrap5FormMetaclass

__all__ = (
	"Bootstrap5ModelFormMetaclass",
	"ModelForm",
	"ModelChoiceField",
	"ModelMultipleChoiceField",
)


def bootstrap5_formfield_callback(field, **kwargs):
	formfield = extensible_formfield_callback(field, **kwargs)
	return _monkey_patch_field(formfield)


class Bootstrap5ModelFormMetaclass(
	Bootstrap5FormMetaclass, ExtensibleModelFormMetaclass
):
	formfield_callback = bootstrap5_formfield_callback

	def bases_check(mcs, bases):
		return bases == (BaseExtensibleModelForm,)


class ModelForm(BaseExtensibleModelForm, metaclass=Bootstrap5ModelFormMetaclass):
	pass


class ModelChoiceField(Bootstrap5FieldMixin, ExtensibleModelChoiceField):
	pass


class ModelMultipleChoiceField(
	Bootstrap5FieldMixin, ExtensibleModelMultipleChoiceField
):
	pass


def modelform_factory(*args, form=ModelForm, **kwargs):
	return extensible_modelform_factory(*args, form=form, **kwargs)
