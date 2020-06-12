import os
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, Index, func, TIMESTAMP, text, tuple_, ForeignKey


metadata = sqlalchemy.MetaData()



TaskResourceSuggestionTable = sqlalchemy.Table(
    demo,
    metadata,
    Column("id", Integer, primary_key=True),

    Column("name", String(length=32), nullable=False),

    Column('updated_at', TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), index=True),
)

