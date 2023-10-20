from django import template as _template
from django.conf import settings as _settings

from b2_utils.helpers import cnpj_parser as _cnpj_parser
from b2_utils.helpers import cpf_parser as _cpf_parser

__all__ = [
    "get_settings",
    "cents_to_brl",
    "cnpj_parse",
    "cpf_parse",
    "index",
    "classname",
    "word",
    "get",
]

register = _template.Library()


@register.simple_tag(name="settings")
def get_settings(name):
    return getattr(_settings, name, "")


def cents_to_brl(quantity):
    try:
        return f"R$ {float(quantity)/100.0}"

    except ValueError:
        return quantity


def cnpj_parse(value: str) -> str:
    return _cnpj_parser(value)


def cpf_parse(cpf_number: str) -> str:
    return _cpf_parser(cpf_number)


def index(my_list, idx):
    try:
        return my_list[idx]
    except (IndexError, TypeError):
        return None


def classname(obj):
    return obj.__class__.__name__


def word(text: str, index: int):
    if text:
        return text.split()[index]

    return None


def get(d: dict, key: str):
    if isinstance(d, dict):
        return d.get(key, None)

    return d


register.filter("brl", cents_to_brl)
register.filter("classname", classname)
register.filter("cnpj", cnpj_parse)
register.filter("cpf", cpf_parse)
register.filter("get", get)
register.filter("index", index)
register.filter("word", word)
