import logging

import requests

import config
from domain.tickets.incidents import Incident

headers = {
    "Content-Type": "application/json",
}


class IncidentAPI(Incident):

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def assign(self, user_matricule):
        if config.execution_mode == "DEV":
            return True

        else:
            url = f"{config.incidents_prefix}/incidents/{self.id}"

            response = requests.put(url, headers=headers, json=user_matricule)

            if response.status_code == 200:
                logging.info("Incident mis à jour")
                return True
            else:
                logging.error(f"Erreur lors de la mise à jour de l'incident : {response.status_code} - {response.text}")
                return False

    @staticmethod
    def get_by_id(incident_id):
        url = f"{config.incidents_prefix}/incidents/{incident_id}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logging.info("Incident récupéré")
            return response.json()
        else:
            logging.error(f"Erreur lors de la récupération de l'incident : {response.status_code} - {response.text}")
            return {}

    @staticmethod
    def get_all():
        if config.execution_mode == "DEV":
            incidents = [
                {
                    "id": "1",
                    "titre": "1412",
                    "statut": "OPEN",
                    "reference": "1",
                    "ticketId": "I1",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 1",
                    "description": "aa lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                    ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                    dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                    sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                    amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": None,
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "2",
                    "titre": "Incident 2",
                    "statut": "OPEN",
                    "reference": "2",
                    "ticketId": "I2",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 1",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": None,
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "3",
                    "titre": "Incident 3",
                    "statut": "OPEN",
                    "reference": "3",
                    "ticketId": "I3",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 1",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": "Personne 1",
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "4",
                    "titre": "Incident 4",
                    "statut": "OPEN",
                    "reference": "4",
                    "ticketId": "I4",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 3",
                    "description": "bb lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": "Personne 1",
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "5",
                    "titre": "8952",
                    "statut": "OPEN",
                    "reference": "5",
                    "ticketId": "I5",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 2",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": None,
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "6",
                    "titre": "Incident 6",
                    "statut": "OPEN",
                    "reference": "6",
                    "ticketId": "I6",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 2",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": "Personne 3",
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "7",
                    "titre": "Incident 7",
                    "statut": "OPEN",
                    "reference": "7",
                    "ticketId": "I7",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 3",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": "Personne 2",
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "8",
                    "titre": "Incident 8",
                    "statut": "OPEN",
                    "reference": "8",
                    "ticketId": "I8",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 1",
                    "description": "zz lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": None,
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "9",
                    "titre": "Incident 9",
                    "statut": "OPEN",
                    "reference": "9",
                    "ticketId": "I9",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 3",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": "Personne 1",
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },
                {
                    "id": "10",
                    "titre": "Incident 10",
                    "statut": "OPEN",
                    "reference": "10",
                    "ticketId": "I10",
                    "createur": "Personne 1",
                    "resolution": None,
                    "cloture": None,
                    "utilisateurAffecte": None,
                    "nomUtilisateurAffecte": None,
                    "impact": "1",
                    "urgence": "1",
                    "department": "Equipe 2",
                    "description": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem \
                                                        ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum \
                                                        dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor \
                                                        sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit \
                                                        amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
                    "assigne": "Personne 2",
                    "image": [
                        "https://escales.ponant.com/wp-content/uploads/2020/12/plage.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Palombaggia.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Pink-Beach.jpg.webp",
                        "https://escales.ponant.com/wp-content/uploads/2021/01/Fakarava.jpg.webp"
                    ],
                    "analysis": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                    "history": ["action 1", "action 2", "action 3"],
                    "remarks": "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem",
                },

            ]

            return incidents

        else:
            url = f"{config.incidents_prefix}/incidents"

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                logging.info("Incidents récupérés")
                return response.json()
            else:
                logging.error(
                    f"Erreur lors de la récupération des incidents : {response.status_code} - {response.text}")
                return []
