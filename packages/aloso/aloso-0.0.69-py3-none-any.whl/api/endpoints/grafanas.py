from fastapi import APIRouter

import config

router = APIRouter(
    prefix="/grafanas",
    tags=["Grafanas"],
)


@router.get("/")
async def get_grafana():
    return {"grafana_prefix": config.grafana_prefix}
