import json
from datetime import datetime

import jwt
from fastapi import APIRouter, Response
from ldap3 import Connection, Server

import config
from api.server.commons import response_personalized
from output.models.activity_logs_database import ActivityLogsData
from output.models.user_database import UserData

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def retrieve_data_user(data: dict):
    name: str = data["name"]
    password: str = data["password"]
    user_auth = False
    token = ""
    response = response_personalized(message="Erreur de connexion, identifiant et / ou mot de passe incorrect",
                                     type_response="Fail")
    if config.connexion_mode == "ldap":
        organization_name = config.ldap_organization_name
        ldap_url_base = f"dc={config.ldap_url_prefix},dc={config.ldap_url_suffix}"
        server = Server(f"ldap://{config.ldap_host}:{config.ldap_port}")

        ldap_connection = Connection(server, user=f"cn={name},ou={organization_name},{ldap_url_base}",
                                     password=password)
        if ldap_connection.bind():
            user_auth = True
            payload = {"username": name, "admin": False, "change_password": False}
            token = jwt.encode(payload=payload, key="VmFndWVseS1FbmdhZ2luZy1PcmJpdC0wMzgzLTY3NzA=", algorithm="HS256")
            response = response_personalized()

    elif config.connexion_mode == "local":
        user = UserData(username=name, password=password)
        user.hash_pass()
        user = user.user_check()
        if user:
            user_auth = True
            payload = {"id_user": user.id, "username": user.username, "admin": user.admin,
                       "change_password": user.change_pwd}
            token = jwt.encode(payload=payload, key="VmFndWVseS1FbmdhZ2luZy1PcmJpdC0wMzgzLTY3NzA=", algorithm="HS256")
            response = response_personalized()

    if user_auth:
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=name,
                                    action="Connexion")
        activity.save()

    return [response, {"token": token}]


@router.post("/sessions")
async def user_logout(data: dict):
    activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                action="Déconnexion")
    activity.save()
