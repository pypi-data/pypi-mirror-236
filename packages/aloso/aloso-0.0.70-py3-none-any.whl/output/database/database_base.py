import logging
from typing import TypeVar, List, Callable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload

import config

engine = create_engine(f'{config.database_resource}:///{config.database_file}')
Session = sessionmaker(bind=engine)()
ClassType = TypeVar('ClassType')


class ModelMethods:

    def save(self, db_session=Session):
        try:
            with db_session as session:
                session.merge(self)
                session.commit()
                logging.info(f"{type(self).__name__} sauvegardé dans la base de données")
                return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde dans la base de données : {e}")
            return False

    def delete(self, db_session=Session):
        try:
            assert self.id is not None
            with db_session as session:
                object_to_delete = session.query(type(self)).filter(type(self).id == self.id).one()
                session.delete(object_to_delete)
                session.commit()
                logging.info(f"{type(self).__name__} supprimé de la base de données")
                return True
        except Exception as e:
            logging.error(f"Erreur lors de la suppression dans la base de données : {e}")
            return False

    @classmethod
    def get_by_id(cls, obj_id: int, db_session=Session, load_related=False):
        try:
            with db_session as session:
                query = session.query(cls).filter(cls.id == obj_id)
                if load_related:
                    query = query.options(joinedload('*'))
                logging.info(f"{cls.__name__} récupéré de la base de données")
                return query.first()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de {cls.__name__} : {e}")
            return None

    @classmethod
    def get_by_name(cls, obj_name: int, db_session=Session, load_related=False):
        try:
            with db_session as session:
                query = session.query(cls).filter(cls.name == obj_name)
                if load_related:
                    query = query.options(joinedload('*'))
                logging.info(f"{cls.__name__} récupéré de la base de données")
                return query.first()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de {cls.__name__} : {e}")
            return None

    @classmethod
    def get_all(cls, db_session=Session, load_related=False):
        try:
            with db_session as session:
                query = session.query(cls)
                if load_related:
                    query = query.options(joinedload('*'))
                logging.info(f"{cls.__name__} : ensemble des objets récupéré de la base de données")
                return query.all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des object : {e}")
            return None

    def link_unlink_base(self, second_relation_objects: List[ClassType], method: Callable[[ClassType], None],
                         db_session=Session):
        try:
            assert self.id is not None
            with db_session as session:
                for obj in second_relation_objects:
                    method(obj)
                session.merge(self)
                session.commit()
                logging.info(f"Lien mis à jour dans la base de données")
                return True
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du lien dans la base de données : {e}")
            return False


Base = declarative_base(cls=ModelMethods)
