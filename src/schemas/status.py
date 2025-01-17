

from datetime import datetime
from pydantic import BaseModel


class AnnouncementSchema(BaseModel):
    message: str
    created_at: datetime | None


class StatusSchema(BaseModel):
    status: str
    version: str
    max_level: int
    characters_online: int
    server_time: datetime
    announcements: list[AnnouncementSchema]
    last_wipe: str
    next_wipe: str


class StatusResponseSchema(BaseModel):
    data: StatusSchema
