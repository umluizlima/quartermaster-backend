import re
from typing import Any
from datetime import datetime as dt


TYPES = {
    str: 'string',
    int: 'integer',
    float: 'float',
    bool: 'boolean',
    list: 'list',
    dict: 'dict',
    type(None): 'null'
}


def check_name(data: dict, key: str) -> Any:
    if key in data and type(data[key]) == str:
        name_regex = re.compile(
            r'\w+( \w+)*'
        )
        if re.fullmatch(name_regex, data[key]) is None:
            return f'campo {key} inválido'
    return None


def check_email(data: dict, key: str) -> Any:
    if key in data and type(data[key]) == str:
        email_regex = re.compile(
            r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        )
        if re.fullmatch(email_regex, data[key]) is None:
            return f'campo {key} inválido'
    return None


def check_datetime(data: dict, key: str) -> Any:
    if key in data and type(data[key]) == str:
        datetime_regex = re.compile(
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'
        )
        if re.fullmatch(datetime_regex, data[key]) is None:
            return f'campo {key} deve ter o formato aaaa-mm-ddThh:mm'
        try:
            data[key] = dt.strptime(data[key], '%Y-%m-%dT%H:%M')
        except ValueError:
            return f'campo {key} inválido'
    return None


def check_phone(data: dict, key: str) -> Any:
    if key in data and type(data[key]) == str:
        phone_regex = re.compile(
            r'(^(\+?[1-9]{1}[0-9]*)?([ -]*[0-9 ]*)+$)'
        )
        if re.fullmatch(phone_regex, data[key]) is None:
            return f'campo {key} inválido'
    return None


def check_data(
    data: dict,
    definition: dict,
    new: bool
) -> Any:
    if len(data) == 0:
        return 'pedido vazio'
    for key, value in data.items():
        if key not in definition['types']:
            return f'campo inválido: {key}'
        if type(value) not in definition['types'][key]:
            tipos = ', '.join([TYPES[t] for t in definition['types'][key]])
            return f"{key} deve ser do(s) tipo(s): {tipos}"
    if new:
        for key in definition['required']:
            if key not in data:
                return f'campo obrigatório: {key}'
    return None
