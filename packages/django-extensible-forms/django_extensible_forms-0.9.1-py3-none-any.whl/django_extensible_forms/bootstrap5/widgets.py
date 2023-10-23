from .. import widgets as extensible_widgets

__all__ = ("MultiWidget",)


class MultiWidget(extensible_widgets.MultiWidget):
	def subwidget_extra_attrs(self, widget):
		extra_attrs = {"class": None}
		match widget.input_type:
			case "select":
				extra_attrs["class"] = "form-select"
			case "checkbox":
				extra_attrs["class"] = "form-check-input"
			case "color":
				extra_attrs["class"] = "form-control-color"
			case "range":
				extra_attrs["class"] = "form-range"
			case _:
				extra_attrs["class"] = "form-control"
		return extra_attrs
