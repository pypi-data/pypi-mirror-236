import ftplib
import logging
from datetime import datetime
from random import randint
from typing import TypeVar
import socket

from sqlalchemy import Column, Integer, String, ForeignKey, inspect, create_engine
from sqlalchemy.orm import sessionmaker, relationship

import config
from domain.equipments_directories import EquipmentsDirectories
from output.database.database_base import Base, engine
from output.shell.configs_shell import ConfigsShell

engine = create_engine(f'{config.database_resource}:///{config.database_file}')
Session = sessionmaker(bind=engine)()
ClassType = TypeVar('ClassType')


class EquipmentsDirectoriesData(Base, EquipmentsDirectories):
    __tablename__ = "EquipmentsDir"

    id = Column(Integer, primary_key=True)
    frequency = Column(Integer, default=1)
    name_equipment_directory = Column(String(50))
    directory_path = Column(String(50), default="")
    server_host = Column(String(50), default="")
    server_user = Column(String(50), default="")

    def is_active(self) -> bool :
        result = True
        try:
            with ftplib.FTP() as connection:
                connection.login(user=self.server_user,
                                 passwd=ConfigsShell.get_value(f"{self.server_host}_{self.server_user}"))
        except Exception:
            result = False

        finally:
            return result

    def connection_and_get_data(self):
        content = self
        try:
            # if self.check_connection_ftp():
            with ftplib.FTP() as connection:
                connection.connect(host=self.server_host)
                connection.login(user=self.server_user,
                                 passwd=ConfigsShell.get_value(f"{self.server_host}_{self.server_user}"))
                content = self.get_most_recent_file_info(connection=connection)

        except Exception as e:
            logging.error(f"Probléme de connexion FTP {e}")

        finally:
            return content

    @staticmethod
    def get_all(session=Session):
        with session:
            return session.query(EquipmentsDirectoriesData).all()

    def get_most_recent_file_info(self, connection: ftplib.FTP):
        self.last_modification_date = datetime.min
        try:
            connection.cwd(self.directory_path)
            files = connection.nlst()

            if not files:
                self.last_modification_date = "Pas de fichier trouvé"
            else:
                recent_file = self.get_recent_file_name(list_files=files)

                if recent_file != "":
                    self.last_modification_date = self.from_file_to_date(filename=recent_file)
                    self.updated_recently = self.was_updated_recently()
                    self.ram_state = self.is_ram_ok()
                    self.cpu_state = self.is_cpu_ok()
                    self.equipment_state = self.is_status_ok()
                else:
                    self.last_modification_date = "Pas de fichier au format YYYYMMDD"

        except Exception as e:
            logging.error(f"Erreur lors de la récupération du fichier le plus récent de {self.directory_path} : {e}")
        finally:
            return self

    def get_ram(self):
        return randint(1, 100)

    # @staticmethod
    def get_cpu(self):
        return randint(1, 100)

    # def get_cpu(self):
    #     try:
    #         with open(config.cpu_file) as file:
    #             data = json.load(file)
    #
    #         for line in data:
    #             if line["equipement"] == self.name:
    #                 return line["cpu_utilisation"]
    #
    #     except IOError as e:
    #         print(f"Erreur lors de la manipulation du fichier '{config.cpu_file}': {e}")
    #
    # def get_ram(self):
    #     try:
    #         with open(config.ram_file) as file:
    #             data = json.load(file)
    #         for line in data:
    #             if line["equipement"] == self.name:
    #                 return line["ram_utilisation"]
    #
    #     except IOError as e:
    #         print(f"Erreur lors de la manipulation du fichier '{config.ram_file}': {e}")
    #

    def was_updated_recently(self) -> bool:
        result = False
        try:
            difference = datetime.now() - datetime.strptime(self.last_modification_date, "%Y-%m-%d")
            if difference.days <= self.frequency:
                result = True
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de la fréquence de mise à jour : {e}")
        finally:
            return result

    # @staticmethod
    # def get_all2():
    #     try:
    #         with sessionmaker(bind=engine)() as session:
    #             data = session.query(EquipmentsDirectoriesData).all()
    #             json_all_directories = {}
    #             for equipment_dir in data:
    #                 json_all_directories[equipment_dir.id] = {
    #                     "id": equipment_dir.id,
    #                     "name_equipment_directory": equipment_dir.name_equipment_directory,
    #                     "directory_path": equipment_dir.directory_path,
    #                     "server_host": equipment_dir.server_host,
    #                     "server_user": equipment_dir.server_user,
    #                     "frequency": equipment_dir.frequency}
    #             return json_all_directories
    #     except Exception as e:
    #         logging.error(e)

    @staticmethod
    def get_equipment_by_id(id_equipment):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(EquipmentsDirectoriesData).filter(
                    EquipmentsDirectoriesData.id == id_equipment).first()
        except Exception as e:
            logging.error(e)

    def create(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.add(self)
                session.commit()
                logging.info("Equipment Directories database : create : ok")
                return True
        except Exception as e:
            logging.error(e)
            return False

    def update(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.merge(self)
                session.commit()
                logging.info("Equipment Directories database : update : ok")
                return True
        except Exception as e:
            logging.error(e)
            return False

    def delete(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.delete(self.get_equipment_by_id(self.id))
                session.commit()
                logging.info("Equipment Directories database : delete : ok")
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    EquipmentsDirectoriesData.get_all()
