class BaseWidgetMutator:
	"""
	Mutates a widget's context before rendering, adding additional templates to render
	in a list along the way. The final call to the render function will always load the
	nested widget template first, and from inside there, it will "unpack" templates
	in the templates list context variable in the reverse order they were added, allowing
	one to effectively nest templates to create highly intricate widgets.
	"""

	def __call__(self, widget):
		self.widget = widget
		widget.render = self.render
		return widget

	def mutate_context(self, context):
		context.setdefault("templates", [self.widget.template_name])
		return context

	def render(self, name, value, attrs=None, renderer=None):
		template_name = "django_extensible_forms/forms/widgets/wrappers/mutated_widget_template.html"
		context = self.mutate_context(self.widget.get_context(name, value, attrs))
		#context["templates"].reverse()  # to get FILO order
		return self.widget._render(template_name, context, renderer)


class DatalistWidgetMutator(BaseWidgetMutator):
	"""Adds an HTML datalist to the widget."""

	def __call__(self, widget, *args, datalist=None, **kwargs):
		widget._datalist = datalist  # the pointer to the datalist elem ID is set in ExtensibleBoundField.build_widget_attrs
		return super().__call__(widget, *args, **kwargs)

	def mutate_context(self, context):
		context = super().mutate_context(context)
		context['widget']["datalist"] = self.widget._datalist  # add the datalist to the context
		context["templates"].append(
			"django_extensible_forms/forms/widgets/wrappers/datalist_wrapper.html"
		)
		return context
