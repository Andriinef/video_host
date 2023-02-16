import datetime
from typing import Optional

import ormar

from .db import database, metadata


class User(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    user_id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=50)


class Video(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    created_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[User] = ormar.ForeignKey(User)
