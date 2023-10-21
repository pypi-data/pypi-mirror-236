import os

import config
from domain.menus import Menus


class MenusShell(Menus):

    @staticmethod
    def menus_replace_file(data):
        value = os.system(f"echo '{data}' > {config.menus_file_path}/{config.menus_file_name}")
        return value == 0

