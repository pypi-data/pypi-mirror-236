import ftplib
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from ftplib import FTP
from typing import ClassVar

import config

import gc

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class TypeEquipments:
    name: str = ""


@dataclass
class Equipments:
    building_id: int = 0
    id_group: int = 0
    id: int = 0
    name: str = ""
    ip: str = ""
    mac: str = ""
    frequency: int = 0
    last_modification_date: str = " "
    # equipment_type: TypeEquipments = field(default_factory=TypeEquipments)
    equipment_dict: ClassVar[dict] = {}
    version: str = ""

    # def connection_and_get_data(self):
    #     pass

    @staticmethod
    def check_ftp_connection(username: str,
                             password: str,
                             host: str):
        pass

    @staticmethod
    def ssh_open_connection(equipment_name):
        pass

    @staticmethod
    def load_all(file_path: str):
        pass

    @staticmethod
    def ftp_get_config_files():
        pass

    @staticmethod
    def new_name_file_from_ftp_dir(file_name: str):
        pass

    @staticmethod
    def get_date_from_ftp_file(file_name: str):
        pass

    @staticmethod
    def recent_date_detection(ftp: FTP):
        pass

    def server_exists(self):
        pass

    @staticmethod
    def get_equipments_version(file_path: str):
        pass

    @staticmethod
    def version_alert(actual_version: str, new_version: str):
        pass

    @staticmethod
    def get_most_recent_file_info(name_group_directory: str, directory_path: str, connection: ftplib.FTP) -> dict[
        str, any]:
        pass

    @staticmethod
    def was_updated_recently(last_modification_date: str, frequency: int) -> bool:
        pass

    @staticmethod
    def get_equipments_directories_files_date_and_size() -> dict:
        pass

    @staticmethod
    def get_equipment_version(command: str):
        pass

    @staticmethod
    def get_all_equipments_versions(command: list):
        pass

    # @staticmethod
    # def get_recent_file_name(list_files: list[str]):
    #     my_recent_file: str = ""
    #     for file in list_files:
    #         if Equipments.is_correctly_formatted(filename=file):
    #             if file.split('_')[0] > my_recent_file.split('_')[0]:
    #                 my_recent_file = file
    #     return my_recent_file
    #
    # @staticmethod
    # def is_correctly_formatted(filename: str):
    #     try:
    #         if time.strptime(filename.split('_')[0], "%Y%m%d"):
    #             return True
    #         return False
    #     except ValueError:
    #         return False
    #
    # @staticmethod
    # def from_file_to_date(filename):
    #     try:
    #         return datetime.strptime(filename.split('_')[0], "%Y%m%d").strftime("%Y-%m-%d")
    #     except ValueError:
    #         return "Erreur"

    # @staticmethod
    # def get_ram(self):
    #     pass
    #
    # # @staticmethod
    # def get_cpu(self):
    #     pass
    #
    # def is_ram_ok(self):
    #     return self.get_ram() < 50
    #
    # def is_cpu_ok(self):
    #     return self.get_cpu() < 50

    # @classmethod
    # def get_general_status(cls):
    #     content = cls.get_equipments_directories_files_date_and_size()
    #     result = True
    #     for key, value in content.items():
    #         if not value.get('line_state'):
    #             result = False
    #     return result
    #
    # def is_status_ok(self):
    #     return (self.is_ram_ok() and self.is_cpu_ok()
    #             and self.was_updated_recently(
    #                 last_modification_date=self.last_modification_date,
    #                 frequency=self.frequency))
