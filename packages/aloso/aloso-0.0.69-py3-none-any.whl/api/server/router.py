from fastapi import APIRouter

from api.endpoints import activities, alias, annuaires, buildings, equipments, favorites, switches, \
    templates, tools, users, incidents, settings, actions, grafanas, equipments_directories
router = APIRouter()
router.include_router(buildings.router)
router.include_router(activities.router)
router.include_router(favorites.router)
router.include_router(tools.router)
router.include_router(annuaires.router)
router.include_router(alias.router)
router.include_router(templates.router)
router.include_router(switches.router)
router.include_router(equipments.router)
router.include_router(incidents.router)
router.include_router(users.router)
router.include_router(settings.router)
router.include_router(actions.router)
router.include_router(grafanas.router)
router.include_router(equipments_directories.router)