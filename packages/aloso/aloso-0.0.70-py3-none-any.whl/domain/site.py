import logging
from dataclasses import dataclass

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class Site:
    id: int
    site_name: str
    contacts: list

    def toggle_site_contact_link(self, contact):
        if contact in self.contacts:
            self.contacts.remove(contact)
        else:
            self.contacts.append(contact)
