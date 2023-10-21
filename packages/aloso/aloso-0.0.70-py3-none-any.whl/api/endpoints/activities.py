from fastapi import APIRouter

from output.models.activity_logs_database import ActivityLogsData

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)


@router.get("/")
async def get_activities():
    return ActivityLogsData.get_all()
