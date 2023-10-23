from .. import utils as extensible_utils

__all__ = ("FieldErrorList", "FieldErrorDict")


class BootstrapFieldErrorMixin:
	def get_context(self):
		context = super().get_context()
		context["error_class"] = "invalid-feedback"
		return context


class FieldErrorList(BootstrapFieldErrorMixin, extensible_utils.FieldErrorList):
	pass


class FieldErrorDict(BootstrapFieldErrorMixin, extensible_utils.FieldErrorDict):
	pass
