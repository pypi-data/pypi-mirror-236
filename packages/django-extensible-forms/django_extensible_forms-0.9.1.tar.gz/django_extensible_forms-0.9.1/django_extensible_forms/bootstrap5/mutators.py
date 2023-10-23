from ..mutators import BaseWidgetMutator

__all__ = ("InputGroupWidgetMutator", "BootstrapInputGroup")


class InputGroupWidgetMutator(BaseWidgetMutator):
	"""Adds span tags before and after the input widget to render Bootstrap input-group-text."""

	def __call__(self, widget, *args, prepend=None, append=None, **kwargs):
		# prepare elements
		if prepend:
			widget._prepend = (
				prepend.split() if hasattr(prepend, "split") else list(prepend)
			)
		if append:
			widget._append = (
				append.split() if hasattr(append, "split") else list(append)
			)
		return super().__call__(widget, *args, **kwargs)

	def mutate_context(self, context):
		context = super().mutate_context(context)
		context["prepend"] = getattr(self, "_prepend", None)
		context["append"] = getattr(self, "_append", None)
		context["templates"].append(
			"django_extensible_forms/bootstrap5_forms/widgets/wrappers/input_group_wrapper.html"
		)
		return context


def BootstrapInputGroup(field, prepend=None, append=None, attrs=None):
	if (
		prepend and (not hasattr(prepend, "__next__") or not hasattr(prepend, "split"))
	) or (append and (not hasattr(append, "__next__") or not hasattr(append, "split"))):
		raise ValueError(
			"%(class)s prepend/append values must be an iterable or a string."
			% {"class": type(field).__name__}
		)
	mutator = InputGroupWidgetMutator()
	field.widget = mutator(field.widget, prepend=prepend, append=append)
	return field
