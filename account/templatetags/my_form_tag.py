from django.template import Library
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
import markdown

register = Library()


@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})

@register.filter(name='addplaceholder')
def addplaceholder(field, placeholder_attr):
    return field.as_widget(attrs={'placeholder': placeholder_attr})

@register.filter(name='addtype')
def addtype(field, type_attr):
    return field.as_widget(attrs={'type': type})

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
