from django.forms.boundfield import BoundField

from .utils import FieldErrorList, RenderableFieldMixin

__all__ = ("ExtensibleBoundField",)

EMPTY_VALUES = {None, ""}


class ExtensibleBoundField(RenderableFieldMixin, BoundField):
	def __init__(self, form, field, name):
		super().__init__(form, field, name)
		self.renderer = form.renderer

	@property
	def template_name(self):
		return self.field.template_name or self.form.renderer.field_template_name

	@property
	def errors(self):
		if hasattr(self.form, "field_error_class"):
			return self.form.errors.get(
				self.name,
				self.form.field_error_class(
					boundfield=self, renderer=self.form.renderer
				),
			)
		return self.form.errors.get(
			self.name,
			FieldErrorList(boundfield=self, renderer=self.form.renderer),
		)

	def get_context(self):
		return {"field": self}

	def build_widget_attrs(self, attrs, widget=None, only_initial=False):
		attrs = super().build_widget_attrs(attrs, widget=widget)
		# set any additional HTML attributes that were given in the Field's
		# constructor (that is, any keyword arguments that are leftover)
		if self.field.attrs:
			for attr, value in self.field.attrs.items():
				attrs[attr] = value
		# set HTML id
		if self.auto_id and "id" not in widget.attrs:
			attrs.setdefault(
				"id", self.html_initial_id if only_initial else self.auto_id
			)
		html_id = attrs.get("id") or widget.attrs.get("id")
		# set CSS classes
		if "class" not in widget.attrs:
			attrs.setdefault("class", self.css_classes())
		# set readonly property if defined
		if self.field.readonly:
			attrs["readonly"] = True
		# set datalist HTML element if defined
		if getattr(self.field.widget, "_datalist", None):
			attrs["list"] = html_id + "Options"
		# set aria-describedby
		if self.errors:
			attrs["aria-describedby"] = html_id + "Feedback"
		elif self.help_text:
			attrs["aria-describedby"] = html_id + "Help"
		return attrs

	# same as django implementation except the setting of HTML id is given to build_widget_attrs()
	# this must be done because several attributes require knowledge of the final HTML id
	def as_widget(self, widget=None, attrs=None, only_initial=False):
		"""
		Render the field by rendering the passed widget, adding any HTML
		attributes passed as attrs. If a widget isn't specified, use the
		field's default widget.
		"""
		widget = widget or self.field.widget
		if self.field.localize:
			widget.is_localized = True
		attrs = attrs or {}
		attrs = self.build_widget_attrs(attrs, widget, only_initial)
		if only_initial and self.html_initial_name in self.form.data:
			# Propagate the hidden initial value.
			value = self.form._widget_data_value(
				self.field.hidden_widget(),
				self.html_initial_name,
			)
		else:
			value = self.value()
		return widget.render(
			name=self.html_initial_name if only_initial else self.html_name,
			value=value,
			attrs=attrs,
			renderer=self.form.renderer,
		)

	def label_tag(self, contents=None, attrs=None, label_suffix=None, tag=None):
		"""Adds CSS classes and attrs to the label tag"""
		attrs = attrs or {}
		if getattr(self.field, "label_attrs", None):
			attrs |= dict(self.field.label_attrs)
		if getattr(self.field, "label_css", None):
			attrs["class"] = set(attrs["class"].split()) if "class" in attrs else set()
			attrs["class"] |= set(
				self.field.label_css.split()
				if hasattr(self.field.label_css, "split")
				else self.field.label_css
			)
			attrs["class"] -= EMPTY_VALUES
			attrs["class"] = " ".join(attrs["class"])
		return super().label_tag(
			contents=contents, attrs=attrs, label_suffix=label_suffix, tag=tag
		)

	def css_classes(self, extra_classes=None):
		"""Adds CSS classes to the input tag"""
		css = set(super().css_classes(extra_classes=extra_classes).split())
		if getattr(self.field, "css", None):
			css |= set(
				self.field.css.split()
				if hasattr(self.field.css, "split")
				else self.field.css
			)
		if self.errors:
			if getattr(self.field, "error_css", None):
				css |= set(
					self.field.error_css.split()
					if hasattr(self.field.error_css, "split")
					else self.field.error_css
				)
			elif getattr(self.form, "field_error_css_class", None):
				css |= set(
					self.form.field_error_css_class.split()
					if hasattr(self.form.field_error_css_class, "split")
					else self.form.field_error_css_class
				)
		css -= EMPTY_VALUES
		return " ".join(css)

	def separator_attrs(self, extra_attrs=None):
		"""Adds CSS classes and attrs to the field separator tag (<div>, <li>, <p>, etc...)"""
		attrs = extra_attrs or {}
		if getattr(self.field, "separator_attrs", None):
			attrs |= dict(self.field.separator_attrs)
		if getattr(self.field, "separator_css", None):
			attrs["class"] = set(attrs["class"].split()) if "class" in attrs else set()
			attrs["class"] |= set(
				self.field.separator_css.split()
				if hasattr(self.field.separator_css, "split")
				else self.field.separator_css
			)
			attrs["class"] -= EMPTY_VALUES
			attrs["class"] = " ".join(attrs["class"])
		if extra_attrs:
			attrs |= dict(extra_attrs)
		return attrs

	def help_text_attrs(self, extra_attrs=None):
		"""Adds CSS classes to the tag containing the help text"""
		attrs = extra_attrs or {}
		if getattr(self.field, "help_text_attrs", None):
			attrs |= dict(self.field.help_text_attrs)
		if getattr(self.field, "help_text_css", None):
			attrs["class"] = set(attrs["class"].split()) if "class" in attrs else set()
			attrs["class"] |= set(
				self.field.help_text_css.split()
				if hasattr(self.field.help_text_css, "split")
				else self.field.help_text_css
			)
			attrs["class"] -= EMPTY_VALUES
			attrs["class"] = " ".join(attrs["class"])
		elif getattr(self.form, "field_help_text_css_class", None):
			attrs["class"] = set(attrs["class"].split()) if "class" in attrs else set()
			attrs["class"] |= set(
				self.form.field_help_text_css_class.split()
				if hasattr(self.form.field_help_text_css_class, "split")
				else self.form.field_help_text_css_class
			)
			attrs["class"] -= EMPTY_VALUES
			attrs["class"] = " ".join(attrs["class"])
		if extra_attrs:
			attrs |= dict(extra_attrs)
		assert "id" not in attrs, (
			"Help text attrs cannot include an HTML id. "
			"You should modify the HTML template instead."
		)
		return attrs
