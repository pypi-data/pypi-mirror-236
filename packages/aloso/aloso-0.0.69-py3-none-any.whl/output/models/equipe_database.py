import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from domain.equipes import Equipe

from output.database.database_base import engine, Base, Session
from output.database.repository import RepositoryDB
from output.models.equipes_users_database import EquipesUsers


class Equipes(Base, Equipe):
    __tablename__ = "Equipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    users = relationship("UserData", secondary="Equipes_Users", back_populates="equipes")

    @property
    def repository(self):
        return RepositoryDB(model=self)

    @classmethod
    def get_all(cls, session=Session):
        try:
            with session:
                data = session.query(Equipes).all()
                json_all_teams = []

                for equipe in data:
                    json_all_teams.append({
                        "id": equipe.id,
                        "name": equipe.name,
                        "users": equipe.get_users_by_equipes_id(),
                    })
                return json_all_teams
        except Exception as e:
            logging.error(e)

    def get_users_by_equipes_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(EquipesUsers).join(Equipes).filter(Equipes.id == self.id).all()
        except Exception as e:
            logging.error(e)

    @classmethod
    def get_by_id(cls, u_id: int, session=Session):
        repository = RepositoryDB(model=cls())
        return repository.get_by_id(obj_id=u_id, db_session=session, load_related=True)

    @staticmethod
    def get_by_name(name_equipe):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(Equipes).filter(Equipes.name == name_equipe).first()
        except Exception as e:
            logging.error(e)
