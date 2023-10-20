from __future__ import annotations

import datetime
import json

from pydantic import BaseModel, Field, field_serializer
from pydantic_db_backend_common.utils import str_to_datetime_if_parseable, utcnow, uid


class LSoftJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

    @classmethod
    def dumps(cls, obj, *args, **kwargs):
        return json.dumps(obj, *args, cls=cls, **kwargs)


class BackendModel(BaseModel):
    uid: str | None = Field(default_factory=uid)
    revision: str | None = None
    version: int | None = 1
    created_time: datetime.datetime | None = Field(default_factory=utcnow)
    updated_time: datetime.datetime | None = Field(default_factory=utcnow)

    # class Config:
    #     json_encoders = {
    #         datetime.datetime: lambda x: x.isoformat(),
    #     }
    #     json_decoders = {
    #         datetime.datetime: str_to_datetime_if_parseable,
    #     }
#
