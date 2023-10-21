import json
import logging

from fastapi import APIRouter, Response, status

import config
from api.server.commons import response_personalized, response
from domain.switch_management import TypeSwitch
from output.shell.equipment_shell import EquipmentShell
from output.shell.script_model_shell import ScriptModelShell
from output.shell.switch_shell import SwitchShell

router = APIRouter(
    prefix="/templates",
    tags=["Templates"],
)


# TODO: change endpoint names in the front
# @app.get("/switches/templates") ok
# @app.post("/switches/template") ok
# @app.post("/templates") ok ? to check
# @app.post("/templates/edition") ok
# @router.post("/templates/equipments") ok

@router.get("/")
async def get_list_templates():
    return ScriptModelShell.get_all_templates_content(templates_directory=config.templates_directory_path)


@router.post("/")
async def create_template(data: dict):
    try:
        name: str = data["type"]
        command: list = data["command"].split("\n")
        variables: dict = {}
        for variable in data["variables"]:
            variables[variable] = ""

        if ScriptModelShell.create_provisioning_templates(file_type=name, command_template=command,
                                                          variables_template=variables):
            return response(class_type="template", operation="création")
        return response(class_type="template", operation="création", type_response="fail")
    except Exception as e:
        return response(class_type="template", operation="création", type_response="fail")


@router.delete("/")
async def remove_template(data: dict):
    try:
        template_name = data["template_name"]
        switch = SwitchShell(switch_type=TypeSwitch(name=template_name.split("_")[0]))

        date: str = f"{template_name.split('_')[1]}_{template_name.split('_')[2]}"

        if ScriptModelShell.remove_template(switch.switch_type.name, date=date):
            return response(class_type="template", operation="suppression")

        return response(class_type="template", operation="suppression", type_response="fail")
    except Exception as e:
        return response(class_type="template", operation="suppression", type_response="fail")


@router.put("/")
async def edit_template(data: dict):
    try:
        name: str = data["templateName"]
        command: list = data["cmd"]
        variables: dict = data["vars"]
        new_variables = {variable: "" for variable in data["newVars"]}
        variables.update(new_variables)

        if ScriptModelShell.modify_template_before_execution(file_name=name,
                                                             command_template=command,
                                                             variables_template=variables):
            return response(class_type="template", operation="création")
        return response(class_type="template", operation="création", type_response="fail")
    except Exception as e:
        return response(class_type="template", operation="création", type_response="fail")


@router.post("/equipments")
async def execution_template_equipments(data: dict):
    equipments_group: dict = data["equipments_group"]
    equipments_group_selected: list = data["selected_equipments_group"]
    file_for_commands: str = data["template_name"]
    data_template: dict = data["values_templates_selected"]

    script_exec = ScriptModelShell()
    list_eq = []
    value = False
    try:
        response = response_personalized(message="Une erreur est survenu lors de l'exécution", type_response="Fail")
        for equipment_gr in equipments_group:
            if equipment_gr in equipments_group_selected:
                for eq in equipments_group[equipment_gr]:
                    if eq['name'] not in equipments_group_selected:
                        equipment = EquipmentShell(name=eq['name'], ip=eq['ip'])
                        list_eq.append(equipment)
        if list_eq:
            script_exec.modify_template_before_execution(file_name=file_for_commands,
                                                         command_template=data_template['commands'],
                                                         variables_template=data_template['variables'])
            if script_exec.exec_commands_on_equipments(file_name=file_for_commands, list_equipments=list_eq):
                response_content = {"message": "Execution terminée !"}
                response_status = 200

        else:
            response_content = {"message": "Veuillez choisir un groupe d'équipement"}
            response_status = 500
        return Response(status_code=response_status, content=json.dumps(response_content),
                        media_type="application/json")

    except Exception as err:
        logging.error(f"une erreur est servenu lors de l'execution {err}")
        response_content = {"message": f"Une erreur est survenu lors de l'exécution"}
        response_status = 500
        return Response(status_code=response_status, content=json.dumps(response_content),
                        media_type="application/json")
