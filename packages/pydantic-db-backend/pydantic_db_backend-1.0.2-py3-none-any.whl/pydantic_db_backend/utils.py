from __future__ import annotations

import datetime
import json

from pydantic_db_backend_common.utils import str_to_datetime_if_parseable


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.try_datetime, *args, **kwargs)

    @staticmethod
    def try_datetime(d):
        ret = {}
        for key, value in d.items():
            if isinstance(value, str):
                ret[key] = str_to_datetime_if_parseable(value)
            else:
                ret[key] = value
        return ret
