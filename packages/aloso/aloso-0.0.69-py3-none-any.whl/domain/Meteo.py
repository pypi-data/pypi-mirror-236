import logging
from dataclasses import dataclass

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class Meteo:

    def CPU(self, cpu_file):
        pass

    def RAM(self, ram_file):
        pass

    def sauvegarde(self):
        pass

    def consolidate_line(self, equipement):
        return equipement["updated_recently"] and equipement["ram_state"] and equipement["cpu_state"]

    def consolidate_page(self, equipements):
        result = True
        for eq in equipements :
            result = (result and self.consolidate_line(eq))
        return result

