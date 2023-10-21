import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from domain.contact import Contact
from output.database.database_base import Base, engine
from output.models.label_database import LabelsContacts
from output.models.site_database import SitesContacts


class Contacts(Base, Contact):
    __tablename__ = "Contacts"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), default='')
    first_name = Column(String(50), default='')
    number = Column(String(50), default='')
    mail = Column(String(50), default='')
    address = Column(String(50), default='')
    commentary = Column(String(150), default='')
    sites = relationship("Sites", secondary="Sites_Contacts", back_populates="contacts", lazy="noload")
    labels = relationship("Labels", secondary="Labels_Contacts", back_populates="contacts", lazy="noload")

    @staticmethod
    def get_all():
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(Contacts).all()
                json_all_contact = {}

                for contact in data:
                    json_all_contact[contact.id] = {
                        "id": contact.id,
                        "last_name": contact.last_name,
                        "first_name": contact.first_name,
                        "number": contact.number,
                        "mail": contact.mail,
                        "address": contact.address,
                        "commentary": contact.commentary,
                        "sites": contact.get_sites_by_contact_id(),
                        "labels": contact.get_labels_by_contact_id()
                    }
                return json_all_contact
        except Exception as e:
            logging.error(e)

    def get_sites_by_contact_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(SitesContacts).join(Contacts).filter(Contacts.id == self.id).all()
                json_sites_by_contact_id = {}

                for site_contact in data:
                    json_sites_by_contact_id[site_contact.site_id] = {
                        "site_id": site_contact.site_id
                    }
                return json_sites_by_contact_id
        except Exception as e:
            logging.error(e)

    def get_labels_by_contact_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(LabelsContacts).join(Contacts).filter(Contacts.id == self.id).all()
                json_label_by_contact_id = {}

                for label_contact in data:
                    json_label_by_contact_id[label_contact.label_id] = {
                        "label_id": label_contact.label_id
                    }
                return json_label_by_contact_id
        except Exception as e:
            logging.error(e)

    def delete(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.query(SitesContacts).filter(SitesContacts.contact_id == self.id).delete()
                session.query(LabelsContacts).filter(LabelsContacts.contact_id == self.id).delete()
                session.delete(self)
                session.commit()
                logging.info(f"Contact supprimé avec succès")
                return True
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du contact : {e}")
            return False
