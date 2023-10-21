import logging

from fastapi import APIRouter

from api.server.commons import response
from output.models.contact_database import Contacts
from output.models.label_database import Labels
from output.models.site_database import SitesContacts, Sites

router = APIRouter(
    prefix="/annuaires",
    tags=["Annuaires"],
)


@router.get("/")
async def get_list_sites_contacts_labels():
    return {"Contacts": Contacts.get_all(), "Sites": Sites.get_all(), "Labels": Labels.get_all()}


@router.post("/contacts")
async def create_contact(data: dict):
    contact = Contacts()

    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.number = data["phone"]
    contact.mail = data["email"]
    contact.address = data["address"]
    contact.commentary = data["comment"]

    if contact.save():
        return response(class_type="contact", operation="création")

    return response(class_type="contact", operation="création", type_response="Fail")


@router.put("/contacts")
async def edit_contact(data: dict):
    contact = Contacts.get_by_id(data.get("id"))

    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.mail = data["mail"]
    contact.address = data["address"]
    contact.number = data["phone"]
    contact.commentary = data["comment"]

    if contact.save():
        return response(class_type="contact", operation="modification")

    return response(class_type="contact", operation="modification", type_response="Fail")


@router.delete("/contacts")
async def supp_contact(data: dict):
    contact = Contacts.get_by_id(data.get("id"))

    if contact.delete():
        return response(class_type="contact", operation="suppression")

    return response(class_type="contact", operation="suppression", type_response="Fail")


@router.post("/sites")
async def create_sites(data: dict):
    site = Sites()

    if data.get("siteName"):
        site.site_name = data.get("siteName")
        site.save()
        return response(class_type="site", operation="création")

    return response(class_type="site", operation="création", type_response="Fail")


@router.delete("/sites")
async def supp_site(data: dict):
    site = Sites.get_by_id(data.get("id"))

    if site.delete():
        return response(class_type="site", operation="suppression")
    return response(class_type="site", operation="suppression", type_response="Fail")


@router.put("/sites")
async def edit_site(data: dict):
    site = Sites.get_by_id(data.get("id"))

    site.site_name = data.get("siteName")

    if site.save():
        return response(class_type="site", operation="modification")
    return response(class_type="site", operation="modification", type_response="Fail")


@router.post("/sites/contacts")
async def add_contact_in_site(data: dict):
    site = Sites.get_by_id(data["siteId"])
    previous_contacts = [contact.id for contact in site.contacts]
    new_contacts = [ids.get("id") for ids in data["contactsList"]]
    contacts_to_add = [contact for contact in new_contacts if contact not in previous_contacts]
    contacts_to_remove = [contact for contact in previous_contacts if contact not in new_contacts]
    final_contacts = contacts_to_add + contacts_to_remove

    try:
        for contact_id in final_contacts:
            site.toggle_site_contact_link(Contacts.get_by_id(contact_id))

        site.save()
        return response(class_type="contacts du site", operation="mise à jour")
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour des contacts du site : {e}")
        return response(class_type="contacts du site", operation="mise à jour", type_response="Fail")


@router.post("/contacts/sites")
async def add_site_in_contact(data: dict):
    contact = Contacts.get_by_id(data.get("contactId"))

    sites = [int(ids) for ids in data["sites"]]
    previous_sites = [ids for ids in contact.get_sites_by_contact_id().keys()]
    sites_to_add = [ids for ids in sites if ids not in previous_sites]
    sites_to_remove = [ids for ids in previous_sites if ids not in sites]

    try:
        if sites_to_add:
            for site_id in sites_to_add:
                site_contact = SitesContacts(site_id=site_id, contact_id=contact.id)
                site_contact.save()

        if sites_to_remove:
            for site_id in sites_to_remove:
                SitesContacts.remove_link_between_contacts_sites(id_site=site_id, id_contact=contact.id)

        return response(class_type="sites du contact", operation="mise à jour")

    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour des sites du contact : {e}")
        return response(class_type="sites du contact", operation="mise à jour", type_response="Fail")
