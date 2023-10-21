from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from domain.label import Label
from output.database.database_base import Base


class Labels(Base, Label):
    __tablename__ = "Labels"

    id = Column(Integer, primary_key=True)
    label_name = Column(String(50))
    contacts = relationship("Contacts", secondary="Labels_Contacts", lazy="immediate")


class LabelsContacts(Base):
    __tablename__ = "Labels_Contacts"
    label_id = Column(Integer, ForeignKey('Labels.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('Contacts.id'), primary_key=True)
