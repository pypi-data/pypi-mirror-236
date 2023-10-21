import json
from datetime import datetime

from fastapi import APIRouter, Response

from api.server.commons import response
from output.models.activity_logs_database import ActivityLogsData
from output.models.favorite_links_database import FavoriteLinksData

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)



@router.get("/")
async def get_favorites():
    return FavoriteLinksData.get_all()


@router.post("/")
async def create_favorites(data: dict):
    name = data["name"]
    url = data["url"]

    favorite = FavoriteLinksData(name=name, url=url)
    favorite.url_to_http(url)
    if favorite.save():
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Ajout du favori {name} | Lien: {url}")
        activity.save()
        return response(class_type="favoris", operation="création", )

    return response(class_type="favoris", operation="création", type_response="Fail")


@router.delete("/")
async def delete_favorites(data: dict):
    # favorite = FavoriteLinksData().get_by_id(data["id"])
    favorite = FavoriteLinksData().get_by_name(data["name"])
    if favorite.delete():
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Suppression du favori {favorite.name} | Lien: {favorite.url}")
        activity.save()
        return response(class_type="favoris", operation="suppression", )

    return response(class_type="favoris", operation="suppression", type_response="Fail")


@router.put("/")
async def update_favorites(data: dict):
    old_favorite = FavoriteLinksData().get_by_name(data["oldName"])
    if data["url"] == "":
        data["url"] = old_favorite.url

    favorite = FavoriteLinksData(id=old_favorite.id, name=data["name"], url=data["url"])
    if favorite.save():
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Modification du favori {favorite.name} | Lien: {favorite.url}")
        activity.save()
        return response(class_type="favoris", operation="modification", )

    return response(class_type="favoris", operation="modification", type_response="Fail")

