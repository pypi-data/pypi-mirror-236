import codecs
import hashlib
import logging
from typing import Optional, List

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship, sessionmaker

from domain.user import User
from output.models.equipe_database import Equipes
from output.models.equipes_users_database import EquipesUsers
from output.database.database_base import Base, Session, engine
from output.database.repository import RepositoryDB


class UserData(Base, User):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), default="")
    password = Column(String(50), default="")
    admin = Column(Boolean, default=False)
    change_pwd = Column(Boolean, default=False)
    matricule = Column(String(50), default="")
    last_name = Column(String(50), default="")
    first_name = Column(String(50), default="")
    equipes = relationship("Equipes", secondary="Equipes_Users", back_populates="users")

    @property
    def repository(self):
        return RepositoryDB(model=self)

    @classmethod
    def get_all(cls, session=Session):
        try:
            with session:
                data = session.query(UserData).all()
                json_all_users = []

                for user in data:
                    json_all_users.append({
                        "id": user.id,
                        "last_name": user.last_name,
                        "first_name": user.first_name,
                        "username": user.username,
                        "password": user.password,
                        "admin": user.admin,
                        "change_pwd": user.change_pwd,
                        "matricule": user.matricule,
                        "teams": user.get_teams_by_user_id(),
                    })
                return json_all_users
        except Exception as e:
            logging.error(e)

    @classmethod
    def get_by_id(cls, u_id: int, session=Session):
        repository = RepositoryDB(model=cls())
        return repository.get_by_id(obj_id=u_id, db_session=session, load_related=True)

    def create(self, session=Session):
        return self.repository.save(db_session=session)

    def update(self, session=Session):
        return self.repository.save(db_session=session)

    def delete(self, session=Session):
        return self.repository.delete(db_session=session)

    def hash_pass(self):
        salt_phrase = f"$2a$12$/dskhjsd"
        hashed_password = hashlib.pbkdf2_hmac(hash_name='sha512', password=self.password.encode('utf-8'),
                                              salt=salt_phrase.encode('utf-8'), iterations=100000)
        encoded_hash = codecs.encode(hashed_password, "base64")
        self.password = encoded_hash

    def user_check(self, session=Session):
        try:
            with session:
                return session.query(UserData).filter(UserData.username == self.username).filter(
                    UserData.password == self.password).first()
        except Exception as e:
            logging.error(e)

    def get_teams_by_user_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(EquipesUsers).join(UserData).filter(UserData.id == self.id).all()
        except Exception as e:
            logging.error(e)




if __name__ == '__main__':
    user = UserData()
    user.username = "admin"
    user.password = "admin"
    user.admin = True
    user.last_name = "Anseur"
    user.first_name = "Meriem"
    user.hash_pass()
    user.create()