import logging
from typing import List, Callable, TypeVar

from sqlalchemy.orm import joinedload

ClassType = TypeVar('ClassType')


class RepositoryDB:
    def __init__(self, model):
        self.model = model

    # OK
    def save(self, db_session):
        try:
            with db_session as session:
                session.merge(self.model)
                session.commit()
                logging.info(f"{type(self.model).__name__} sauvegardé dans la base de données")
                return True
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la sauvegarde dans la base de données : {e}")
            return False

    # OK
    def delete(self, db_session):
        try:
            assert self.model.id is not None
            with db_session as session:
                object_to_delete = session.query(type(self.model)).filter(type(self.model).id == self.model.id).one()
                session.delete(object_to_delete)
                session.commit()
                logging.info(f"{type(self.model).__name__} supprimé de la base de données")
                return True
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la suppression dans la base de données : {e}")
            return False

    # OK
    def get_by_id(self, db_session, obj_id, load_related=False):
        try:
            with db_session as session:
                query = session.query(type(self.model)).filter(type(self.model).id == obj_id)
                if load_related:
                    query = query.options(joinedload('*'))
                logging.info(f"{type(self.model).__name__} récupéré de la base de données")
                return query.first()
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la récupération de {type(self.model).__name__} : {e}")
            return None

    # OK
    def get_all_obj(self, db_session, load_related=False):
        try:
            with db_session as session:
                query = session.query(type(self.model))
                if load_related:
                    query = query.options(joinedload('*'))
                logging.info(f"{type(self.model).__name__} ensemble des objets récupéré de la base de données")
                return query.all()
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la récupération des object : {e}")
            return None

    def link(self, db_session, second_relation_objects: List[ClassType], method: Callable[[ClassType], None]):
        try:
            assert self.model.id is not None
            with db_session as session:
                for obj in second_relation_objects:
                    method(obj)
                session.merge(self.model)
                session.commit()
                logging.info(f"Lien mis à jour dans la base de données")
                return True
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la mise à jour du lien dans la base de données : {e}")
            return False
