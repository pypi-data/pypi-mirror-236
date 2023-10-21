import logging
from dataclasses import dataclass

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class Contact:
    id: int
    last_name: str
    first_name: str
    number: str
    mail: str
    address: str
    commentary: str
    sites: list
    labels: list

    @staticmethod
    def get_all():
        pass

    def get_sites_by_contact_id(self):
        pass

    def get_labels_by_contact_id(self):
        pass
