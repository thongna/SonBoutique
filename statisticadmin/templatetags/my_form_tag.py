from django.template import Library

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