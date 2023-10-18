from typing import Sequence, Mapping, Union, Any

RAISE_ERROR = "RAISE_ERROR"

KeyListType = Union[Sequence[str], str]

_parse_keys = lambda ks: ks.split(" ") if isinstance(ks, str) else ks


def pop_keys(data: dict, keys: KeyListType) -> dict:
    """
    从字典中弹出指定的键值对，这些键值对将从字典中被移除，返回由指定的键值对组成的新的字典。
    """
    return {k: data.pop(k) for k in _parse_keys(keys) if k in data}


def assign(target: dict, source: dict) -> None:
    """
    将 source 字典中的键值对写到 target 字典中，已经存在的键值对将会被覆盖，target 字典会被修改
    """
    for k, v in source.items():
        target[k] = v


def pick(data: Union[dict, object], keys: KeyListType) -> dict:
    """
    从对象或者字典中取出指定的属性或者键，返回一个新的字典
    """
    if isinstance(data, dict):
        return {k: data[k] for k in _parse_keys(keys) if k in data}
    else:
        return {k: getattr(data, k) for k in _parse_keys(keys) if k in data}


def pick_with_defaults(data: dict, defaults: Mapping[str, Any]):
    """
    从对象或者字典中取出指定的属性或者键，返回一个新的字典。
    属性或者键不存在时返回默认值。
    """
    if isinstance(data, dict):
        return {k: data.get(k, v) for k, v in defaults.items()}
    else:
        return {k: getattr(data, k) if hasattr(data, k) else v for k, v in defaults.items()}
