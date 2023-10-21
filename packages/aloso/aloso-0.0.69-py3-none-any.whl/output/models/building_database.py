from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

import config
from domain.building import Building
from output.database.database_base import Base
from output.shell.shell import Shell


class BuildingData(Base, Building):
    __tablename__ = "Building"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    equipments = relationship("EquipmentsData", back_populates="building", lazy="immediate")

    def execute(self, *args):
        conn = Shell.ssh_connection(host=self.equipment.ip,
                                    username=config.ssh_equipment_username,
                                    password=config.ssh_equipment_password,
                                    port=config.ssh_equipment_port)

        cmd = "energywise query importance 75 name set level 10" if args[0] is None else args[0]

        try:
            with conn:
                conn.run(cmd)
            print(f"Commande {cmd} executé avec succès")
        except Exception as e:
            print(f"Erreur d'execution de la commande : {e}")
