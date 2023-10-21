from dataclasses import dataclass


@dataclass
class Incident:
    id: int
    reference: str = ""
    titre: str = ""
    description: str = ""
    image: str = ""
    departementId: str = ""
    ticketId: str = ""
    statut: str = ""
    createur: str = ""
    assigne: str = ""
    resolution: str = ""
    cloture: str = ""
    utilisateurAffecte: str = ""
    nomUtilisateurAffecte: str = ""
    impact: str = ""
    priorite: str = ""

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def assign(self, user_matricule):
        pass

    @staticmethod
    def get_by_id(incident_id):
        pass

    @staticmethod
    def get_all():
        pass
