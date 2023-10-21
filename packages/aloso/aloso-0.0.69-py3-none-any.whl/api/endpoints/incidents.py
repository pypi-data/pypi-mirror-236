from fastapi import APIRouter

from output.external_api.tickets.incident_impl import IncidentAPI

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.get("/")
async def get_incidents():
    return IncidentAPI.get_all()


@router.patch("/")
async def assign_user(data: dict):
    user_to_assign = {"assigne": data["userMatricule"]}
    incident = IncidentAPI(id=data["incidentId"])
    incident.assign(user_to_assign)
    print(user_to_assign)
