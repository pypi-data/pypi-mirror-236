import logging
from dataclasses import dataclass
from typing import Union
import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class ConfigsManagement:
    config_file_path: str = ""
    variable_name: str = ""
    variable_value: Union[str, int] = None

    def edit_variable(self):
        pass
