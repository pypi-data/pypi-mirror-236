import json

from fastapi import APIRouter, Response

import config
from api.server.commons import response, response_personalized
from output.models.equipe_database import Equipes
from output.models.equipments_directories_database import EquipmentsDirectoriesData
from output.models.user_database import UserData
from output.shell.configs_shell import ConfigsShell
from output.shell.data_backup_shell import BackupShell
from output.shell.equipment_shell import EquipmentShell
from output.shell.menus_shell import MenusShell

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get("/")
async def get_settings():
    return {
        "connexionMode": config.connexion_mode,
        "ldapHost": config.ldap_host,
        "ldapPort": config.ldap_port,
        "ldapPrefix": config.ldap_url_prefix,
        "ldapSuffix": config.ldap_url_suffix,
        "ldapOrganizationName": config.ldap_organization_name,

        "appName": config.application_name,  # os.getenv("APPLICATION_NAME"),
        "frontHost": config.frontend_host,
        "nvmURL": config.nvm_wget_url,

        "ansibleUsername": config.ansible_username,
        "ansiblePort": config.ansible_port,
        "ansibleHost": config.ansible_host,

        "ftpHost": config.ftp_host,
        "ftpUsername": config.ftp_username,
        "ftpDir": config.equipement_ftp_remote_directory,
        "ftpPwd": ConfigsShell.get_value('ftp_password'),

        "switchLocalDir": config.switch_configs_local_directory,
        "switchRemoteGit": config.repository_to_save_configs_for_all_switches_with_ssh,
        "savingHour": config.saving_hour,

        "inventoryDir": config.inventory_local_directory,
        "inventoryFileName": config.inventory_file_name,
        "inventoryVersion": config.inventory_file_version,
        "inventorySeparator": config.separateur,
        "EquipmentsPort": config.equipments_port,
        "EquipmentsPwd": ConfigsShell.get_value('equipments_password'),

        "DNSType": config.DNS_type,
        "aliasFile": config.alias_file,
        "configPath": f"{config.root_dir}/config.py",

        "logs_path": config.logs_file_path,
        "logs_level": config.debug_level,
        "database_resource": config.database_resource,
        "database_file": config.database_file,
        "excel_file": config.excel_file_path,
        "template_dir": config.templates_directory_path,

        "grafanaPrefix": config.grafana_prefix,
        "incidentsPrefix": config.incidents_prefix,

        "envPath": config.env_path,

        "backupUsername": config.backup_username,
        "backupPort": config.backup_port,
        "backupHost": config.backup_host,
        "backupTargetDir": config.backup_target_dir,
        "backupHour": config.backup_hour
    }


@router.post("/equipes/users")
async def link_teams_users(data: dict):
    equipe_id = data.get('equipe_id')
    list_id_users = data.get('list_id_users')
    list_users = []

    if equipe_id:
        equipe = Equipes.get_by_id(equipe_id)
        for new_id in list_id_users:
            user = UserData.get_by_id(new_id)
            list_users.append(user)

        if equipe.link_unlink_base(second_relation_objects=list_users, method=equipe.toggle_equipe_user_link):
            return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour des liens",
                                 type_response="Fail")


@router.get("/equipes")
async def get_equipes():
    equipes = Equipes()
    return equipes.get_all()


@router.post("/equipes")
async def add_equipe(data: dict):
    if Equipes.get_by_name(data['name']):
        return response(class_type="Equipe", operation="création", type_response="Fail")
    else:
        equipe = Equipes(name=data['name'])
        equipe.save()
        return response(class_type="Equipe", operation="création", type_response="Success")


@router.delete("/equipes")
async def delete_equipes(data: dict):
    equipe = Equipes.get_by_id(data['idEquipe'])
    if equipe:
        equipe.delete()
        return response(class_type="Equipe", operation="Suppression")
    return response(class_type="Equipe", operation="Suppression", type_response="Fail")


@router.put("/equipes")
async def modify_equipe(data: dict):
    if Equipes.get_by_id(data['idEquipe']):
        equipe = Equipes.get_by_id(data['idEquipe'])
        equipe.name = data['name']
        equipe.save()
        return response(class_type="Equipe", operation="modification")
    return response(class_type="Equipe", operation="modification", type_response="Fail")


@router.post("/local")
async def change_user_data():
    configuration = ConfigsShell()
    configuration.config_file_path = f"{config.root_dir}/config.py"
    configuration.variable_name = "connexion_mode"
    configuration.variable_value = "local"
    if configuration.edit_variable():
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/ldap")
async def change_ldap_param(data: dict):
    configuration = ConfigsShell()
    configuration.config_file_path = f"{config.root_dir}/config.py"
    response_api = response_personalized(
        message="Un problème est survenu lors de la mise à jour du fichier de configuration",
        type_response="Fail")
    if data['ldapPort'] is None:
        data['ldapPort'] = ""

    ldap_dict = {
        "ldap_host": data['ldapHost'],
        "ldap_url_prefix": data['ldapPrefix'],
        "ldap_url_suffix": data['ldapSuffix'],
        "ldap_port": data['ldapPort'],
        "ldap_organization_name": data['ldapOrgName'],
        "connexion_mode": "ldap",
    }
    for key, value in ldap_dict.items():
        configuration.variable_name = key
        configuration.variable_value = value
        if configuration.edit_variable():
            response_api = response_personalized()

    return response_api


@router.get("/users")
async def get_user_settings():
    return UserData.get_all()


@router.post("/users")
async def add_user(data: dict):
    if data['username'] != "" and data['new_pwd'] != "":
        user = UserData(username=data['username'], password=data['new_pwd'])
        # print(user)
        if not user.get_by_id(data['username']):
            if data['admin']:
                user.admin = data['admin']
            if data['change_pwd_next']:
                user.change_pwd = data['change_pwd_next']
            user.matricule = data['matricule']
            user.last_name = data['last_name']
            user.first_name = data['first_name']
            user.hash_pass()
            user.create()
            return response(class_type="Utilisateur", operation="création")

    return response(class_type="Utilisateur", operation="création", type_response="Fail")


@router.put("/users")
async def modify_user(data: dict):
    response = response_personalized(message=" Un problème est survenu lors de la modification de l'utilisateur",
                                     type_response="Fail")
    if data.get("personalEdit"):
        user = UserData.get_by_id(data.get('user_id'))
        if user:
            user.password = data.get("newPassword")
            user.hash_pass()
            user.change_pwd = False
            user.update()
            response = response_personalized(message="Mot de passe modifié avec succés !")
        else:
            response = response_personalized(message="Mot de passe actuel incorrect !", type_response="Fail")
    else:
        if data['username'] != '':
            user = UserData.get_by_id(data['idUser'])
            user.username = data['username']
            user.admin = bool(data['admin'])
            user.change_pwd = bool(data['change_pwd_next'])
            if data['newPassword'] is not None and data['newPassword'] != '':
                user.password = data['newPassword']
                user.hash_pass()
            user.matricule = data['matricule']
            user.last_name = data.get('last_name')
            user.first_name = data.get('first_name')
            user.update()
            response = response_personalized(message="Utilisateur modifié avec succés !")

    return response


@router.delete("/users")
async def delete_user(data: dict):
    user = UserData.get_by_id(data['idUser'])

    if user:
        user.delete()
        return response(class_type="Utilisateur", operation="Suppression")

    return response(class_type="Utilisateur", operation="Suppression", type_response="Fail")


@router.post("/users/equipes")
async def link_user_teams(data: dict):
    user_id = data.get('user_id')
    list_id_teams = data.get('list_id_teams')
    list_teams = []

    if user_id:
        user = UserData.get_by_id(user_id)
        for new_id in list_id_teams:
            team = Equipes.get_by_id(new_id)
            list_teams.append(team)

        if user.link_unlink_base(second_relation_objects=list_teams, method=user.toggle_user_equipe_link):
            return response_personalized()
    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier des liens",
                                 type_response="Fail")


@router.post("/front")
async def front_param(data: dict):
    front_dict = {
        "application_name": data['application_name'],
        "frontend_host": data['front_host'],
        "nvm_wget_url": data['nvm_url']
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(front_dict):
        return response_personalized()

    return response_personalized(
        message="Un problème est survenu lors de la mise à jour du fichier de configuration",
        type_response="Fail")


@router.post("/ftp")
async def ftp_param(data: dict):
    ftp_dict = {
        "ftp_host": data['ftp_host'],
        "ftp_username": data['ftp_username'],
        "equipement_ftp_remote_directory": data['ftp_dir']
    }
    configuration = ConfigsShell()
    value = configuration.modify_from_dict(ftp_dict)
    if value:
        configuration.update_salt('ftp_password', data['ftp_password'])
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/switches")
async def switches_settings_param(data: dict):
    switchs_dict = {
        "switch_configs_local_directory": data['switch_local_dir'],
        "repository_to_save_configs_for_all_switches_with_ssh": data['switch_remote_git'],
        "saving_hour": data['saving_hour']
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(switchs_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/ansible")
async def ansible_settings_param(data: dict):
    if data['ansible_port'] is None:
        data['ansible_port'] = ""
    ansible_dict = {
        "ansible_host": data['ansible_host'],
        "ansible_port": data['ansible_port'],
        "ansible_username": data['ansible_username']
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(ansible_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/equipments")
async def equipments_param(data: dict):
    if data['equipments_port'] is None:
        data['equipments_port'] = ""
    equipments_dict = {
        "inventory_local_directory": data['inventory_local_directory'],
        "inventory_file_name": data['inventory_file_name'],
        "inventory_file_version": data['inventory_file_version'],
        "equipments_port": data['equipments_port'],
        "separateur": data['separateur']
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(equipments_dict):
        configuration.update_salt('equipments_password', data['equipments_password'])
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/alias")
async def alias_settings_param(data: dict):
    alias_dict = {
        "DNS_type": data['DNS_type'],
        "alias_file": data['alias_file'],
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(alias_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/environments")
async def project_env_param(data: dict):
    alias_dict = {
        "env_path": data['env_path']
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(alias_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/logs")
async def logs_settings_param(data: dict):
    if data['debug_level'] is None:
        data['debug_level'] = ""
    logs_dict = {
        "debug_level": data['debug_level'],
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(logs_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/others")
async def others_settings_param(data: dict):
    db_dict = {
        "templates_directory_path": data['templates_directory_path'],
        "excel_file_path": data['excel_file_path'],
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(db_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/backup")
async def backup_param(data: dict):
    if data['backup_port'] is None:
        data['backup_port'] = ""
    backup_dict = {
        "backup_hour": data['backup_hour'],
        "backup_target_dir": data['backup_target_dir'],
        "backup_username": data['backup_username'],
        "backup_port": data['backup_port'],
        "backup_host": data['backup_host']
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(backup_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/monitoring")
async def add_equipment_sub_directories(data: dict):
    try:
        equipment_dir = EquipmentsDirectoriesData(directory_path=data['directory_path'],
                                                  name_equipment_directory=data['name_equipment_directory'],
                                                  server_user=data['server_user'],
                                                  server_host=data['server_host'],
                                                  )
        if data.get('frequency'):
            equipment_dir.frequency = data['frequency']

        if equipment_dir.create():
            ConfigsShell.create_salt(name=f"{data.get('server_host')}_{data.get('server_user')}",
                                     value=data.get('password'))
            return response_personalized(message="Nouvelle configuration créée avec succès !")
        else:
            return response_personalized(
                message="Un problème est survenu lors de l'ajout des paramètres pour le monitoring",
                type_response="Fail")

    except Exception as err:
        print(err)
        return response_personalized(
            message="Un problème est survenu lors de l'ajout des paramètres pour le monitoring",
            type_response="Fail")


@router.put("/monitoring")
async def modify_equipment_sub_directories(data: dict):
    try:
        response_api = response_personalized(
            message="Un problème est survenu lors de la modification des paramètres pour le monitoring",
            type_response="Fail")
        equipment_dir = EquipmentsDirectoriesData.get_equipment_by_id(id_equipment=data['id'])
        if equipment_dir:
            equipment_dir.frequency = data['frequency']
            equipment_dir.directory_path = data['directory_path']
            equipment_dir.name_equipment_directory = data['name_equipment_directory']
            equipment_dir.server_user = data['server_user']
            equipment_dir.server_host = data['server_host']
            if equipment_dir.update():
                if data.get('password'):
                    ConfigsShell.update_salt(name=f"{data.get('server_host')}_{data.get('server_user')}", value=data.get('password'))
                response_api = response_personalized(message="Modification effectuée avec succès !")

        return response_api
    except Exception as err:
        return response_personalized(
            message="Un problème est survenu lors de la modification des paramètres pour le monitoring",
            type_response="Fail")


@router.delete("/monitoring")
async def delete_equipment_sub_directories(data: dict):
    equipment_dir = EquipmentsDirectoriesData.get_equipment_by_id(data['idEq'])
    if equipment_dir:
        equipment_dir.delete()
        return response_personalized(message="Suppression effectuée avec succès !")

    return response_personalized(
        message="Un problème est survenu lors de la suppression des paramètres pour le monitoring",
        type_response="Fail")


@router.get("/versions")
async def get_package_version():
    return ConfigsShell.get_version_package()


@router.post("/backups")
async def backup_execute(data: dict):
    if data['backup_port'] is None:
        data['backup_port'] = ""

    backup_dict = {
        "backup_hour": data['backup_hour'],
        "backup_target_dir": data['backup_target_dir'],
        "backup_username": data['backup_username'],
        "backup_port": data['backup_port'],
        "backup_host": data['backup_host']
    }
    configuration = ConfigsShell()
    configuration.modify_from_dict(backup_dict)
    if BackupShell.check_ssh_connection(username=data['backup_username'], host=data['backup_host'],
                                        port=data['backup_port']):
        BackupShell.backup()
        return response_personalized(message="Sauvegarde effectuée avec succès !")

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/backups/connections")
async def verify_backup_server_connection(data: dict):
    host = data['host']
    port = data.get('port')
    username = data['username']

    if BackupShell.check_ssh_connection(username=username, host=host, port=port):
        return response_personalized(message="Connexion au serveur de backup réussie !")

    return response_personalized(message="Un problème est survenu lors de la connexion au serveur de backup",
                                 type_response="Fail")


@router.post("/ftps/connections")
async def verify_ftp_server_connection(data: dict):
    host = data['host']
    username = data['username']
    pwd = data.get('pwd')
    if not pwd:
        pwd = ConfigsShell.get_value(f"{host}_{username}")
    if EquipmentShell.check_ftp_connection(username=username, host=host, password=pwd):
        return response_personalized(message="Connexion au serveur FTP réussie !")

    return response_personalized(
        message=f"Un problème est survenu lors de la connexion au serveur FTP ({host}:21, {username})",
        type_response="Fail")


@router.post("/menus")
async def menus_update_file(data: dict):
    data_menus = data['menus']

    if MenusShell.menus_replace_file(data=data_menus):
        return response_personalized(message="Menus mis à jour avec succès !")

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/grafanas")
async def grafana_settings_param(data: dict):
    grafana_dict = {
        "grafana_prefix": data['grafana_prefix'],
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(grafana_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")


@router.post("/incidents")
async def incidents_settings_param(data: dict):
    grafana_dict = {
        "incidents_prefix": data['incidents_prefix'],
    }
    configuration = ConfigsShell()
    if configuration.modify_from_dict(grafana_dict):
        return response_personalized()

    return response_personalized(message="Un problème est survenu lors de la mise à jour du fichier de configuration",
                                 type_response="Fail")
