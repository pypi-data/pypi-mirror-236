from dataclasses import dataclass
from datetime import datetime


@dataclass
class Actions:
    id: str = ""
    description: str = ""
    typeAction: str = ""
    dateAction: str = ""
    udsAction: str = ""
    auteur: str = ""
    cause: str = ""
    ciCause: str = ""
    ticketId: str = ""  # équipe de la personne au moment où elle fait l'action

    def set_action_attributes(self, user_matricule, description, ticket_id, type_action):
        self.auteur = user_matricule
        self.dateAction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.typeAction = type_action
        self.description = description
        self.ticketId = ticket_id

    def resolve(self, user_matricule, description, ticket_id):
        self.set_action_attributes(user_matricule=user_matricule, description=description, ticket_id=ticket_id,
                                   type_action="RESOLUTION")

    def close(self, user_matricule, description, ticket_id):
        self.set_action_attributes(user_matricule=user_matricule, description=description, ticket_id=ticket_id,
                                   type_action="CLOTURE")

    def analyze(self, user_matricule, description, ticket_id):
        self.set_action_attributes(user_matricule=user_matricule, description=description, ticket_id=ticket_id,
                                   type_action="ANALYSE")

    def apply_action(self, type_action, user_matricule, ticket_id, analysis):
        if type_action == "RESOLUTION":
            self.resolve(user_matricule=user_matricule, ticket_id=ticket_id, description=analysis)
        elif type_action == "CLOTURE":
            self.close(user_matricule=user_matricule, ticket_id=ticket_id, description=analysis)
        elif type_action == "ANALYSE":
            self.analyze(user_matricule=user_matricule, ticket_id=ticket_id, description=analysis)
