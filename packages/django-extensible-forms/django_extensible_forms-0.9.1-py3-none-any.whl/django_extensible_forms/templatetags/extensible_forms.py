from django import template

__all__ = ("pop",)

register = template.Library()


@register.filter
def pop(stack: list):
	return stack.pop()
