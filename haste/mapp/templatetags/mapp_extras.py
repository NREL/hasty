from django import template

register = template.Library()


@register.filter
def concat_protos(proto_list):
    """concatenate arg1 & arg2"""
    return proto_list.replace(' ', '-')
