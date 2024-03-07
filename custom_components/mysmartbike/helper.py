"""Helpers for the MySmartBike integration."""
from __future__ import annotations

import datetime
from enum import Enum
import inspect
import json
import time
from typing import Dict, Optional, Union

from .const import JSON_EXPORT_IGNORED_KEYS, LOGGER


def get_class_property_names(obj: object):
    """Return the names of all properties of a class."""
    return [
        p[0]
        for p in inspect.getmembers(type(obj), inspect.isdatadescriptor)
        if not p[0].startswith("_")
    ]


def parse_datetime(date_str: str) -> Optional[datetime.datetime]:
    """Convert a time string into datetime."""
    if not date_str:
        return None
    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for date_format in date_formats:
        try:
            # Parse datetimes using `time.strptime` to allow running in some embedded python interpreters.
            # https://bugs.python.org/issue27400
            time_struct = time.strptime(date_str, date_format)
            parsed = datetime.datetime(*(time_struct[0:6]))
            if time_struct.tm_gmtoff and time_struct.tm_gmtoff != 0:
                parsed = parsed - datetime.timedelta(seconds=time_struct.tm_gmtoff)
            parsed = parsed.replace(tzinfo=datetime.UTC)
            return parsed
        except ValueError:
            pass
    LOGGER.error("unable to parse '%s' using %s", date_str, date_formats)
    return None


class MBJSONEncoder(json.JSONEncoder):
    """JSON Encoder that handles data classes, properties and additional data types."""

    def default(self, o) -> Union[str, dict]:  # noqa: D102
        if isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
            return o.isoformat()
        if not isinstance(o, Enum) and hasattr(o, "__dict__") and isinstance(o.__dict__, Dict):
            retval: Dict = o.__dict__
            retval.update({p: getattr(o, p) for p in get_class_property_names(o)})
            return {k: v for k, v in retval.items() if k not in JSON_EXPORT_IGNORED_KEYS}
        return str(o)
