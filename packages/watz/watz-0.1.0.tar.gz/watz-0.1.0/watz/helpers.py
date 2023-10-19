"""Miscellaneous helper functions."""
import datetime as dt
import typing as tp
from collections import deque
from decimal import Decimal
from types import GeneratorType

import orjson
from pydantic import BaseModel


def serialize(obj: tp.Any) -> bytes:
    """A wrapper on `orjson.dumps()` to include all configuration options for handling all supported types.

    Args:
        obj: The object to serialize to json.

    Returns:
        bytes: The serialized json bytes blob.
    """
    return orjson.dumps(
        obj,
        option=orjson.OPT_SERIALIZE_NUMPY
        | orjson.OPT_SERIALIZE_DATACLASS
        | orjson.OPT_SERIALIZE_UUID
        | orjson.OPT_NAIVE_UTC,  # Make dts without timezone info default to UTC
        # Fallback to the python func on types orjson doesn't support:
        default=_orjson_extras,
    )


def dump(
    obj: tp.Any,
) -> tp.Any:
    """Dumps all pydantic models in an arbitrary object to dicts. As a side effect iterables are all downcast to lists. Useful when models exist in e.g. a list.

    Args:
        obj: The object to dump.

    Returns:
        tp.Any: The dumped object.
    """
    if isinstance(obj, BaseModel):
        return dump(obj.model_dump())

    if isinstance(obj, dict):
        return {dump(key): dump(value) for key, value in obj.items()}

    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
        return [dump(item) for item in obj]

    return obj


def _orjson_extras(obj: tp.Any) -> tp.Any:
    """Handle the extra cases orjson doesn't serialise by default."""
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, dt.timedelta):
        return obj.total_seconds()
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, Decimal):
        return float(obj)

    raise TypeError


def _all_supported_types_example() -> tuple[list[tp.Any], bytes]:
    import dataclasses as dc

    import numpy as np  # type: ignore
    from pydantic.dataclasses import dataclass as pd_dataclass

    @dc.dataclass
    class ExampleDataclass:
        """Example dataclass."""

        a: int
        b: str

    @pd_dataclass
    class ExamplePdDataclass:
        """Example pydantic dataclass."""

        a: int
        b: str

    class ExamplePdModel(BaseModel):
        """Example pydantic model."""

        a: int
        b: str

    now = dt.datetime.now()
    all_types = [
        1,  # ints
        1.5,  # floats
        "2",  # strings
        now,  # datetimes
        now.date(),  # dates
        now.time(),  # times
        dt.timedelta(days=1),  # timedeltas
        np.array([1, 2, 3]),  # numpy arrays
        True,  # bools
        None,  # None/null
        ["nested"],  # lists
        {"nested": "nested"},  # dicts
        {"set"},  # sets
        (4, 5, 6),  # tuples
        ExampleDataclass(a=7, b="8"),  # dataclasses
        ExamplePdDataclass(a=9, b="10"),  # pydantic dataclasses
        ExamplePdModel(a=11, b="12"),  # pydantic models
        Decimal("13.14"),  # decimals
    ]

    return all_types, serialize(all_types)
