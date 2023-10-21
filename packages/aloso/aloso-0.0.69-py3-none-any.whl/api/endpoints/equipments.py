import json
import logging
import string

from fastapi import APIRouter, Response
from sqlalchemy import false

import config
from api.server.commons import response, response_personalized
from output.external_api.cisco_prime_output import CiscoPrimeOutput
from output.models.equipments_database import EquipmentsData
from output.models.equipments_directories_database import EquipmentsDirectoriesData
from output.models.equipments_group_database import EquipmentsGroupData
from output.shell.equipment_demo import EquipmentDemo
from output.shell.equipment_shell import EquipmentShell

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
)


@router.get("/groups/primes")
async def get_cisco_prime_equipments():
    return CiscoPrimeOutput.get_all_devices()

@router.get("/groups")
async def get_equipments_and_groups():
    # V1.0 : Inventory
    # inventory_path = config.inventory_local_directory
    # inventory_name = config.inventory_file_name
    # return EquipmentShell.load_all(f"{inventory_path}/{inventory_name}")
    # V2.0 : Database
    return EquipmentsGroupData.get_all()


@router.post("/groups")
async def create_equipments_group(data: dict):
    new_equipment_group = data["new_equipment"]
    try:
        values: str = data["values"]
        list_equipment_group_values = values.split('\n')

        if new_equipment_group != '':
            # V1.0 : Inventory
            # new_group_of_equipments = EquipmentShell()
            # value = new_group_of_equipments.create(name_group=new_equipment_group,
            #                                        list_values=list_equipment_group_values)
            # V2.0 : Database
            new_group_of_equipments = EquipmentsGroupData()
            new_group_of_equipments.new_group_and_equipments(new_name_group=new_equipment_group,
                                                             list_equipments=list_equipment_group_values)

            return response(class_type=f"groupe d'équipement {new_equipment_group}", operation="création")

    except Exception as err:
        logging.info(f"Une erreur est survenu lors de l'ajout du groupe d'équipements {err}")
        return response(class_type=f"groupe d'équipement {new_equipment_group}", operation="création",
                        type_response="Fail")


@router.put("/groups")
async def edit_equipments_and_group(data: dict):
    equipment_group_selected = data["equipment_selected"]

    try:
        values: str = data["values"]
        id_group_selected = data["id_group_selected"]
        list_equipment_group_values = values.split('\n')

        if equipment_group_selected != '':
            # V1.0 : Inventory
            # edit_group_of_equipments = EquipmentShell()
            # value = edit_group_of_equipments.edit(name_group=equipment_group_selected,
            #                                       list_values=list_equipment_group_values)
            # V2.0 : Database
            new_group_of_equipments = EquipmentsGroupData.get_group_equipment_by_id(id_group_selected)
            EquipmentsGroupData.update_group_and_equipments(my_group=new_group_of_equipments,
                                                            name_group=equipment_group_selected,
                                                            list_values=list_equipment_group_values)

            return response(class_type=f"groupe d'équipement {equipment_group_selected}", operation="modification")

    except Exception as err:
        logging.info(f"Une erreur est survenu lors de la modification du groupe d'équipements {err}")
        return response(class_type=f"groupe d'équipement {equipment_group_selected}", operation="modification",
                        type_response="Fail")


@router.delete("/groups")
async def delete_equipments_group(data: dict):
    equipment_group_to_remove = data["group_selected"]

    try:
        if equipment_group_to_remove != '':
            # V1.0 : Inventory
            # remove_group_of_equipments = EquipmentShell()
            # value = remove_group_of_equipments.remove(name_group=equipment_group_to_remove)
            # V2.0 : Database
            id_group_selected = data["id_group_selected"]
            my_group = EquipmentsGroupData.get_group_equipment_by_id(id_group_selected)
            my_group.delete()
            return response(class_type=f"groupe d'équipement {equipment_group_to_remove}", operation="suppression")

    except Exception as err:
        logging.info(f"Une erreur est survenu lors de la suppression du groupe d'équipements {err}")
        return response(class_type=f"groupe d'équipement {equipment_group_to_remove}", operation="suppression",
                        type_response="Fail")


@router.get("/")
async def get_equipments():
    return EquipmentsData.get_all()


@router.post("/")
async def create_equipment(data: dict):
    id_group = data["id_group_selected"]
    values: str = data["values"]
    name_equipment = values.split(' ')[0]
    try:
        if id_group is not None:
            new_equipment = EquipmentsData(name=name_equipment, ip=values.split(' ')[1])
            new_equipment.group = EquipmentsGroupData.get_group_equipment_by_id(id_group)
            new_equipment.create()

        return response(class_type=f"équipement {name_equipment}", operation="création")

    except Exception as err:
        logging.info(f"Une erreur est survenu lors de la créeation de l'équipements {err}")
        return response(class_type=f"'équipement {name_equipment}", operation="création", type_response="Fail")


@router.put("/")
async def update_equipment(data: dict):
    id_equipment = data.get("id_equipment_selected")
    name_group = data.get("name_group_selected")
    values: str = data.get("values")
    name_equipment = values.split(' ')[0]
    print("je suis appele")

    try:

        if id_equipment is not None:
            my_equipment = EquipmentsData.get_equipment_by_id(id_equipment)
            if my_equipment is not None:
                my_equipment.name = name_equipment
                my_equipment.ip = values.split(' ')[1]
                my_equipment.update()

            return response(class_type=f"équipement  {name_equipment} dans {name_group}", operation="modification", )

    except Exception as err:
        logging.info(f"Une erreur est survenu lors de la modification de l'équipements {err}")
        return response(class_type=f"équipement : {name_equipment} dans {name_group}", operation="modification",
                        type_response="Fail")


@router.delete("/")
async def delete_equipment(data: dict):
    id_equipment = data["id_equipment_selected"]
    name_equipment = data["name_equipment_selected"]
    name_group = data["name_group_selected"]

    try:
        if id_equipment is not None:
            my_equipment = EquipmentsData.get_equipment_by_id(id_equipment)
            my_equipment.delete()
            return response(class_type=f"équipement  {name_equipment} dans {name_group}", operation="suppression", )

    except Exception as err:
        logging.info(f"Une erreur est survenu lors de la suppression de l'équipements {err}")
        return response(class_type=f"équipement : {name_equipment} dans {name_group}", operation="suppression",
                        type_response="Fail")


@router.post("/connections")
async def verify_equipment_server_connection(data: dict):
    host = data['host']
    username = data['username']
    group = data['equipment_group']
    port = config.equipments_port

    if data['port'] is not None:
        port = data['port']

    if EquipmentShell.check_ssh_equipments_connection(username=username, host=host, port=port, equipment_group=group):
        return response_personalized(message=f"Connexion à {username} ({host}:{port}) dans {group} réussie")

    return response_personalized(
        message=f" Un problème est survenu lors de la connexion à {username} ({host}:{port}) dans {group}",
        type_response="Fail")


# @router.get("/directories")
# async def get_equipments_directories():
#     return EquipmentsDirectoriesData.get_all2()

@router.get("/versions")
async def get_equipments_diff_versions():
    return EquipmentShell.version_alert(
        actual_version=f"{config.inventory_local_directory}/{config.inventory_file_name}",
        new_version=f"{config.inventory_local_directory}/{config.inventory_file_version}")

@router.get("/directories/files/status")
async def get_equipments_general_status():
    return EquipmentShell.get_general_status()
#

# @router.get("/directories/files")
# async def get_equipments_directories_files():
#     return EquipmentShell.get_equipments_directories_files_date_and_size()




