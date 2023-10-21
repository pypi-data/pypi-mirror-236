import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from domain.site import Site
from output.database.database_base import Base, engine


class Sites(Base, Site):
    __tablename__ = "Sites"

    id = Column(Integer, primary_key=True)
    site_name = Column(String(50))
    contacts = relationship("Contacts", secondary="Sites_Contacts", lazy="immediate", back_populates="sites")


class SitesContacts(Base):
    __tablename__ = "Sites_Contacts"
    site_id = Column(Integer, ForeignKey('Sites.id'), primary_key=True) # ondelete="CASCADE"
    contact_id = Column(Integer, ForeignKey('Contacts.id'), primary_key=True)

    @staticmethod
    def remove_link_between_contacts_sites(id_site, id_contact):
        try:
            with sessionmaker(bind=engine)() as session:
                session.query(SitesContacts).filter(SitesContacts.site_id == id_site,
                                                    SitesContacts.contact_id == id_contact).delete()
                session.commit()
        except Exception as e:
            logging.error(e)
