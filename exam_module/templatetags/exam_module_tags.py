from django import template

register = template.Library()

@register.filter(name='ends_with_int')
def text_ends_with_int(value, int_value):
    if value.name.endswith(str(int_value)):
        return value


@register.filter(name='value_from_key')
def dictionary_value_from_key(dictionary, key):

    try:
        value = dictionary.get(str(key))
        return value
    except AttributeError:
        return "None"
