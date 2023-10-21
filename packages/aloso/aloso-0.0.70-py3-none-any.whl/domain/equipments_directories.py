import ftplib
import logging
from dataclasses import dataclass
import time
from datetime import datetime

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class EquipmentsDirectories:
    name_equipment_directory: str
    directory_path: str
    server_host: str
    server_user: str
    # server_password: str
    frequency: int
    last_modification_date: str = "Erreur de connexion"
    ram_state: bool = False
    cpu_state: bool = False
    equipment_state: bool = False
    updated_recently: bool = False

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def connection_and_get_data(self):
        pass

    def get_most_recent_file_info(self, connection):
        pass

    @staticmethod
    def get_recent_file_name(list_files: list[str]):
        my_recent_file: str = ""
        for file in list_files:
            if EquipmentsDirectories.is_correctly_formatted(filename=file):
                if file.split('_')[0] > my_recent_file.split('_')[0]:
                    my_recent_file = file
        return my_recent_file

    @staticmethod
    def is_correctly_formatted(filename: str):
        try:
            if time.strptime(filename.split('_')[0], "%Y%m%d"):
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def from_file_to_date(filename):
        try:
            return datetime.strptime(filename.split('_')[0], "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            return "Erreur"

    def get_ram(self):
        pass

    def get_cpu(self):
        pass

    def is_ram_ok(self):
        return self.get_ram() < 50

    def is_cpu_ok(self):
        return self.get_cpu() < 50

    def is_status_ok(self):
        return (self.is_ram_ok() and self.is_cpu_ok()
                and self.was_updated_recently())

    @classmethod
    def get_general_status(cls):
        content = cls.get_all()
        result = True
        for equipment in content:
            if not equipment.equipment_state:
                result = False
        return result
