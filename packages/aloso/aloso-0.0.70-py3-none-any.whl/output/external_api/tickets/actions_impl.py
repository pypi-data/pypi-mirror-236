import logging

import requests

import config
from domain.tickets.actions import Actions

headers = {
    "Content-Type": "application/json",
}


class ActionsAPI(Actions):

    def save(self):
        if config.execution_mode == "DEV":
            return True

        else:
            url = f"{config.incidents_prefix}/actions"

            response = requests.post(url, headers=headers, json=self.__dict__)

            if response.status_code == 200:
                logging.info("Action mise à jour")
                return True
            else:
                logging.error(f"Erreur lors de la mise à jour de l'action : {response.status_code} - {response.text}")
                return False
