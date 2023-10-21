from sqlalchemy import Column, Integer, ForeignKey

from output.database.database_base import Base


class EquipesUsers(Base):
    __tablename__ = "Equipes_Users"

    equipe_id = Column(Integer, ForeignKey('Equipes.id'),primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'),primary_key=True)
