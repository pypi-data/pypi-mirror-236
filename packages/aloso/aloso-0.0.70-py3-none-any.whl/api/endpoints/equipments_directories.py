from fastapi import APIRouter
import logging
from output.models.equipments_directories_database import EquipmentsDirectoriesData

router = APIRouter(
    prefix="/equipmentsDirectories",
    tags=["EquipmentsDirectories"],
)


@router.get("/directories/files")
async def get_equipments_directories_files():
    content = {}
    for equipment in EquipmentsDirectoriesData.get_all():
        if equipment.is_active():
            content[equipment.directory_path] = equipment.connection_and_get_data()
        else:
            content[equipment.directory_path] = equipment
    return content


@router.get("/directories/files/status")
async def get_equipments_general_status():
    return EquipmentsDirectoriesData.get_general_status()


@router.get("/directories")
async def get_equipments_directories():
    content = []
    for equipment in EquipmentsDirectoriesData.get_all():
        equi = {
            "id": equipment.id,
            "name_equipment_directory": equipment.name_equipment_directory,
            "directory_path": equipment.directory_path,
            "server_host": equipment.server_host,
            "server_user": equipment.server_user,
            "frequency": equipment.frequency}
        content.append(equi)
    return content
    # return EquipmentsDirectoriesData.get_all()
