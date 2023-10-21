import json
from datetime import datetime

from fastapi import APIRouter, Query, Response

from api.server.commons import response
from output.models.activity_logs_database import ActivityLogsData
from output.record_dns_bind9 import Bind9
from output.shell.equipment_shell import EquipmentShell

router = APIRouter(
    prefix="/alias",
    tags=["Alias"],
)


@router.get("/")
def check_alias(alias_name: str = Query(...)):
    # TODO récuperation liste des alias
    alias = Bind9()
    alias.open_data = ["alias", "switch", "montre", "sel", "souris"]
    alias.name = alias_name

    return alias.alias_is_available()


@router.get("/hosts")
async def check_host(host_name: str = Query(...)):
    equipment = EquipmentShell()
    equipment.name = host_name

    return equipment.server_exists()


@router.post("/")
async def create_alias(data: dict):
    alias = Bind9()
    alias.name = data["alias_name"]
    alias.host = data["host_name"]
    # alias.create_alias()
    value = True  # depends on method create_alias()

    if value:
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Création de l'alias {alias.name} vers {alias.host}")
        activity.save()
        return response(class_type="Alias "+alias.name, operation="création")

    return response(class_type="Alias "+alias.name, operation="création", type_response="Fail")


if __name__=="__main__":
    print(check_alias("alias"))