from datetime import datetime, date
import json


class DateTimeAwareEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"type": "datetime", "data": obj.isoformat()}
        if isinstance(obj, date):
            return {"type": "date", "data": obj.isoformat()}
        return super(json.JSONEncoder, self).default(obj)


class DateTimeAwareDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.default_object_hook, *args, **kwargs
        )

    def default_object_hook(self, obj):
        if "type" in obj and "data" in obj:
            if obj["type"] == "datetime":
                return datetime.fromisoformat(obj["data"])
            if obj["type"] == "date":
                return date.fromisoformat(obj["data"])
        return obj
