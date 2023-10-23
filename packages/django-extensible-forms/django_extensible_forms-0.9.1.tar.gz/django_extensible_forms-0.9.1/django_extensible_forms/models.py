from django.core.exceptions import FieldError, ImproperlyConfigured
from django.forms.models import (
	ALL_FIELDS,
	BaseModelForm,
	ModelChoiceField as DjangoModelChoiceField,
	ModelFormOptions,
	ModelMultipleChoiceField as DjangoModelMultipleChoiceField,
	fields_for_model,
	modelform_factory as django_modelform_factory,
	apply_limit_choices_to_to_formfield,
)

from .fields import ExtensibleFieldMixin, _monkey_patch_field
from .forms import (
	ExtensibleFormMetaclass,
	ExtensibleFormMixin,
	ExtensibleFormOptions,
)
from .mutators import DatalistWidgetMutator

__all__ = (
	"BaseExtensibleModelForm",
	"ModelForm",
	"ExtensibleModelFormMetaclass",
	"ExtensibleModelFormOptions",
	"ModelChoiceField",
	"ModelMultipleChoiceField",
)

INVALID_DATALIST_INPUTS = {
	None,
	"hidden",
	"password",
	"checkbox",
	"radio",
	"button",
	"submit",
	"select",
}


def extensible_formfield_callback(field, **formfield_kwargs):
	formfield = _monkey_patch_field(field.formfield(**formfield_kwargs))
	# narrow choices down before any attempt at formulating a datalist
	apply_limit_choices_to_to_formfield(formfield)
	if (
		getattr(formfield.widget, "input_type", None) not in INVALID_DATALIST_INPUTS
		and getattr(formfield, "choices", None) is not None
	):
		mutator = DatalistWidgetMutator()
		formfield.widget = mutator(formfield.widget, datalist=formfield.choices)
	return formfield


class ExtensibleModelFormOptions(ExtensibleFormOptions):
	attrs = ExtensibleFormOptions.attrs + (
		"model",
		"fields",
		"exclude",
		"widgets",
		"labels",
		"help_texts",
		"error_messages",
		"field_classes",
		"formfield_callback",
	)

	def __init__(self, options=None):
		ModelFormOptions.__init__(self, options)
		super().__init__(options)
		self.formfield_callback = getattr(options, "formfield_callback", None)


class ExtensibleModelFormMetaclass(ExtensibleFormMetaclass):
	formfield_callback = extensible_formfield_callback

	def bases_check(mcs, bases):
		return bases == (BaseExtensibleModelForm,)

	def get_meta_opts_class():
		return ExtensibleModelFormOptions

	def construct_class(mcs, opts, new_class):
		super().construct_class(mcs, opts, new_class)
		# We check if a string was passed to `fields` or `exclude`,
		# which is likely to be a mistake where the user typed ('foo') instead
		# of ('foo',)
		for opt in ["fields", "exclude"]:
			value = getattr(opts, opt)
			if isinstance(value, str) and value != ALL_FIELDS:
				msg = (
					"%(model)s.Meta.%(opt)s cannot be a string. "
					"Did you mean to type: ('%(value)s',)?"
					% {
						"model": new_class.__name__,
						"opt": opt,
						"value": value,
					}
				)
				raise TypeError(msg)

		if opts.model:
			# If a model is defined, extract form fields from it.
			if opts.fields is None and opts.exclude is None:
				raise ImproperlyConfigured(
					"Creating a ModelForm without either the 'fields' attribute "
					"or the 'exclude' attribute is prohibited; form %s "
					"needs updating." % new_class.__name__
				)

			if opts.fields == ALL_FIELDS:
				# Sentinel for fields_for_model to indicate "get the list of
				# fields from the model"
				opts.fields = None

			fields = fields_for_model(
				opts.model,
				opts.fields,
				opts.exclude,
				opts.widgets,
				opts.formfield_callback or mcs.formfield_callback,
				opts.localized_fields,
				opts.labels,
				opts.help_texts,
				opts.error_messages,
				opts.field_classes,
				# should be done in formfield_callback
				apply_limit_choices_to=False,
			)

			# make sure opts.fields doesn't specify an invalid field
			none_model_fields = {k for k, v in fields.items() if not v}
			missing_fields = none_model_fields.difference(new_class.declared_fields)
			if missing_fields:
				message = "Unknown field(s) (%s) specified for %s"
				message = message % (", ".join(missing_fields), opts.model.__name__)
				raise FieldError(message)
			# Override default model fields with any custom declared ones
			# (plus, include all the other declared fields).
			fields.update(new_class.declared_fields)
		else:
			fields = new_class.declared_fields

		new_class.base_fields = fields

	def configure_field_localization(mcs, meta, new_class):
		pass

	def configure_help_texts(mcs, meta, new_class):
		pass


class BaseExtensibleModelForm(ExtensibleFormMixin, BaseModelForm):
	pass


class ModelForm(BaseExtensibleModelForm, metaclass=ExtensibleModelFormMetaclass):
	pass


class ModelChoiceField(ExtensibleFieldMixin, DjangoModelChoiceField):
	pass


class ModelMultipleChoiceField(ExtensibleFieldMixin, DjangoModelMultipleChoiceField):
	pass


def modelform_factory(*args, form=ModelForm, **kwargs):
	return django_modelform_factory(*args, form=form, **kwargs)
