import os
from production.configurations import config_files_data

if __name__ == '__main__':
    # Config sample
    with(open('config.py', 'w')) as file:
        file.write(config_files_data.config_sample)
    if os.path.exists('config.py'):
        from output import directories

    # Create directories
    directories.create_base_dir()

    if os.path.exists('logs') and os.path.exists('data'):
        from output.database.database_base import Base, engine
        from output.models.contact_database import Contact
        from output.models.site_database import Site, SitesContacts
        from output.models.label_database import Label, LabelsContacts
        from output.models.favorite_links_database import FavoriteLinksData
        from output.models.activity_logs_database import ActivityLogsData
        from output.models.user_database import UserData
        from output.models.equipments_directories_database import EquipmentsDirectoriesData
        from output.models.building_database import BuildingData
        from output.models.equipments_group_database import EquipmentsGroupData
        from output.models.equipments_database import EquipmentsData
        from output.models.equipes_users_database import EquipesUsers
        from output.models.equipe_database import Equipes

    # Empty database
    Base.metadata.create_all(engine)

    if not UserData.get_all():
        new_user = UserData(username="admin", password="admin", admin=True)
        new_user.hash_pass()
        new_user.create()

    if os.path.exists('config.py'):
        from output.shell.configs_shell import ConfigsShell

    ConfigsShell.generate_clear_salt()
    ConfigsShell.generate_salt_file()
