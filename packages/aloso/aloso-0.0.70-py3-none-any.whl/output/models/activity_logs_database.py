from sqlalchemy import Column, Integer, String

from domain.activity_logs import ActivityLogs
from output.database.database_base import Base


class ActivityLogsData(Base, ActivityLogs):
    __tablename__ = "ActivityLogs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(String(50))
    author = Column(String(50))
    action = Column(String(50))
