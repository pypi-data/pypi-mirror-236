import decimal
import json
from datetime import datetime, date
from typing import Any
import numbers


class DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o) if o % 1 == 0 else float(o)
        if isinstance(o, datetime):
            return o.__str__()
        if isinstance(o, date):
            return o.__str__()
        super(DefaultEncoder, self).default(o)


def default_encoder(o: Any) -> Any:
    if isinstance(o, decimal.Decimal):
        return int(o) if o % 1 == 0 else float(o)
    if isinstance(o, datetime):
        return o.__str__()
    if isinstance(o, date):
        return o.__str__()
    if hasattr(o, "__dict__"):
        return o.__dict__
    raise TypeError(f"Object {o} of type {o.__class__} can't be serialized by the JSON encoder")
