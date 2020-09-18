from django import template

register = template.Library()


@register.filter
def concat_protos(proto_list):
    """concatenate arg1 & arg2"""
    return proto_list.replace(' ', '-')

# @register.filter
# def list_all_tags()


@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except BaseException:
        return None
