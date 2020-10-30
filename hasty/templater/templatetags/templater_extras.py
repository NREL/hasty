from django import template

register = template.Library()


@register.filter
def get_item(fault_object, map):
    return map.get(fault_object)


@register.filter
def reverse_get_item(equipment_object, map):
    to_return = []
    for k, v in map.items():
        if equipment_object in v:
            to_return.append(k)
    return to_return
