import json
from random import randint

from config import cpu_file, ram_file
from domain.equipment_management import Equipments


class EquipmentDemo(Equipments):

    def get_ram(self):
        return randint(1, 100)

    # @staticmethod
    def get_cpu(self):
        return randint(1, 100)
