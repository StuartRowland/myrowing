from django import template
register = template.Library()

@register.filter(name='access')
def access(value, argument):
	return value[argument]