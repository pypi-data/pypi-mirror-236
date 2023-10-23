from django.forms import widgets as django_widgets

__all__ = ("IndeterminateCheckboxInput", "RangeInput", "MultiWidget")


class IndeterminateCheckboxInput(django_widgets.CheckboxInput):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# TODO: set indeterminate value on creation
		self.attrs["oninput"] = "event.target.value = event.target.checked.toString();"

	def format_value(self, value, *args, **kwargs):
		return "true" if self.check_test(value) else ""

	def value_from_datadict(self, data, files, name, *args, **kwargs):
		if name not in data:
			return None
		value = data.get(name)
		if isinstance(value, str):
			value = value.lower()
		choices = {"true": True, "false": False, "on": True, "off": False}
		return choices.get(value)

	def value_omitted_from_data(self, data, files, name, *args, **kwargs):
		return None


class RangeInput(django_widgets.Input):
	input_type = "range"
	template_name = "extensible_forms/widgets/range.html"
	min = 0
	max = 0

	def get_context(self, name, value, attrs):
		context = super().get_context(name, value, attrs)
		context["widget"]["min"] = self.min() if callable(self.min) else self.min
		context["widget"]["max"] = self.max() if callable(self.max) else self.max
		return context


class MultiWidget(django_widgets.MultiWidget):
	# identical to django implementation except modified to allow
	# subwidgets to set their own attributes
	def get_context(self, name, value, attrs):
		context = super(django_widgets.MultiWidget, self).get_context(
			name, value, attrs
		)
		if self.is_localized:
			for widget in self.widgets:
				widget.is_localized = self.is_localized
		# value is a list/tuple of values, each corresponding to a widget
		# in self.widgets.
		if not isinstance(value, (list, tuple)):
			value = self.decompress(value)

		# change: only store values with truthiness, so we don't overwrite subwidget attrs later w/ blanks
		final_attrs = {
			key: value for key, value in context["widget"]["attrs"].items() if value
		}
		input_type = final_attrs.pop("type", None)
		id_ = final_attrs.get("id")
		subwidgets = []
		for i, (widget_name, widget) in enumerate(
			zip(self.widgets_names, self.widgets)
		):
			if input_type is not None:
				widget.input_type = input_type
			widget_name = name + widget_name
			try:
				widget_value = value[i]
			except IndexError:
				widget_value = None
			widget_attrs = widget.build_attrs(
				widget.attrs,
				extra_attrs=(self.subwidget_extra_attrs(widget) | final_attrs),
			)
			if id_:
				widget_attrs["id"] = "%s_%s" % (id_, i)
			subwidgets.append(
				widget.get_context(widget_name, widget_value, widget_attrs)["widget"]
			)
		context["widget"]["subwidgets"] = subwidgets
		return context

	def subwidget_extra_attrs(self, widget):
		return {}
