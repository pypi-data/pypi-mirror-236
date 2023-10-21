import logging
from dataclasses import dataclass

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class Equipe:
    id: int
    name: str
    users = []

    def toggle_equipe_user_link(self, user):
        if user in self.users:
            self.users.remove(user)
        else:
            self.users.append(user)
