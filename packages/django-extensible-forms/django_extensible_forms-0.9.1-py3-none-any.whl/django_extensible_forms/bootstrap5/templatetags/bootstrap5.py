from django import template
from django.forms import Form
from django.forms.fields import Field
from django.forms.boundfield import BoundField

from ..fields import _monkey_patch_field

__all__ = ("bootstrapify",)

register = template.Library()


@register.filter
def bootstrapify(obj: Form | BoundField):
	if isinstance(obj, Form):
		form = obj
		for field in form.fields.values():
			_monkey_patch_field(field)
		return form
	elif isinstance(obj, BoundField):
		form = obj.form
		field = obj.field
		_monkey_patch_field(field)
		bf = field.get_bound_field(form, obj.name)
		form._bound_fields_cache[obj.name] = bf
		return bf
