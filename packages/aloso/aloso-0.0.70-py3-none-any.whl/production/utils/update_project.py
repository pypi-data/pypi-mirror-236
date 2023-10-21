import os

import config
from output.models.user_database import UserData
from output.shell.configs_shell import ConfigsShell
from output.shell.create_services import create_backup_service, create_backend_service, create_watch_config_service, \
    create_nginx_service

if __name__ == "__main__":
    update_finished = "\033[1m\033[32mMise à jour terminée\033[0m"
    update_failed = "\033[1m\033[31mUne erreur est survenue lors de la mise à jour\033[0m"

    # Config file update
    project_root = os.path.abspath(os.getcwd())
    env_folder = os.path.join(project_root, 'direnv')
    config_sample_path = ConfigsShell.find_sample_file(env_folder)
    config_file_path = os.path.join(project_root, "config.py")

    try:
        print("\033[1m\033[32mMise à jour du fichier de configuration en cours...\033[0m")
        ConfigsShell.update_production_config_file(sample_file_path=config_sample_path,
                                                   config_file_path_to_update=config_file_path)
        print(update_finished)
    except Exception as e:
        print(f"{update_failed}: {e}")

    # Database init main user
    print("\n\033[1m\033[32mUtilisateur base de données principal en cours de vérification...\033[0m")
    if not UserData.get_all():
        new_user = UserData(username="admin", password="admin", admin=True)
        new_user.hash_pass()
        new_user.create()
        print("\033[1m\033[32mUtilisateur principal créé\033[0m")
    else:
        print("\033[1m\033[33mUtilisateur principal déjà existant\033[0m")

    # Services creation
    print("\n\033[1m\033[32mMise à jour des services en cours...\033[0m")
    main_directory = config.root_dir
    env = config.env_path
    server_ip = config.api_server_ip
    server_port = config.api_server_port

    create_backup_service(working_directory=main_directory,
                          exec_start=f"/bin/bash -c 'source {main_directory}/{env}/activate && python3 {main_directory}/scheduled_backup.py'")

    create_backend_service(working_directory=main_directory,
                           exec_start=f"{main_directory}/{env}/gunicorn api.server.main:app -k uvicorn.workers.UvicornWorker --bind {server_ip}:{server_port} --access-logfile {main_directory}/logs/access_log.log --error-logfile {main_directory}/logs/error_log.log --log-level debug")

    create_watch_config_service(working_directory=main_directory,
                                exec_start=f"{main_directory}/{env}/watchmedo shell-command --patterns=\"config.py\" --command=\"kill -HUP $(systemctl status backend |  sed -n 's/.*Main PID: \(.*\)$/\1/g p' | cut -f1 -d' ')\" {main_directory}")

    create_nginx_service()
    print(update_finished)

    # Database updates
    print("\n\033[1m\033[32mVérification des mises à jour des tables de la base de données en cours...\033[0m")
    try:
        print(update_finished)
    except Exception as e:
        print(f"{update_failed}: {e}")
