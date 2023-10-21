import json

from fastapi import APIRouter, Response

from api.server.commons import response
from output.external_api.tickets.actions_impl import ActionsAPI

router = APIRouter(
    prefix="/actions",
    tags=["Actions"],
)


@router.post("/")
async def create_action(data: dict):
    user_matricule = data.get("userMatricule")
    description = data.get("description")
    ticket_id = data.get("ticketId")
    type_action = data.get("typeAction")
    analysis = data.get("analysis")

    action = ActionsAPI()

    action.apply_action(type_action=type_action, user_matricule=user_matricule, ticket_id=ticket_id, analysis=analysis)

    if action.save():
        return response(class_type="Action", operation="création")

    return response(class_type="Action", operation="création", type_response="Fail")
