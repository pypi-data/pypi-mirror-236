import os
import subprocess


def create_service(service_name, service_file_content):
    try:
        service_file_path = f"/etc/systemd/system/{service_name}.service"
        if os.path.isfile(service_file_path):
            print(f"\033[1m\033[33mLe service {service_name} existe déjà !\033[0m")
            return

        assert os.path.isdir("/etc/systemd/system"), "/etc/systemd/system directory does not exist"

        with open(service_file_path, "w") as f:
            f.write(service_file_content)

        subprocess.run(["sudo", "systemctl", "daemon-reload"])
        subprocess.run(["sudo", "systemctl", "enable", service_name])
        subprocess.run(["sudo", "systemctl", "start", service_name])

        print(f"\033[1m\033[32mService {service_name} créé avec succès !\033[0m")
    except Exception as e:
        print(f"\033[91mUne erreur est survenue lors de la création du service {service_name}: {e}\033[0m")


def create_backup_service(working_directory, exec_start, service_name="backup"):
    service_file_content = f"""[Unit]
Description=Sauvegarde automatique du dossier data
After=network.target

[Service]
Group=sudo
WorkingDirectory={working_directory}
ExecStart={exec_start}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

    create_service(service_name, service_file_content)


def create_backend_service(working_directory, exec_start, service_name="backend"):
    service_file_content = f"""[Unit]
Description=Gunicorn Daemon for FastAPI Application
After=network.target

[Service]
Group=sudo
WorkingDirectory={working_directory}
ExecStart={exec_start}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

    create_service(service_name, service_file_content)


# watchdog==3.0.0
def create_watch_config_service(working_directory, exec_start, service_name="watch-config"):
    service_file_content = f"""[Unit]
Description=Service qui surveille les modifications du fichier de configuration pour relancer le serveur NGINX
After=network.target

[Service]
Group=sudo
WorkingDirectory={working_directory}
ExecStart={exec_start}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

    create_service(service_name, service_file_content)


def create_nginx_service(service_name="nginx"):
    service_file_content = f"""# Stop dance for nginx
# =======================
#
# ExecStop sends SIGSTOP (graceful stop) to the nginx process.
# If, after 5s (--retry QUIT/5) nginx is still running, systemd takes control
# and sends SIGTERM (fast shutdown) to the main process.
# After another 5s (TimeoutStopSec=5), and if nginx is alive, systemd sends
# SIGKILL to all the remaining processes in the process group (KillMode=mixed).
#
# nginx signals reference doc:
# http://nginx.org/en/docs/control.html
#
[Unit]
Description=Serveur principal pour le projet réseau (frontend, backend, backup)
Documentation=man:nginx(8)
Wants=backend.service backup.service watch-config.service
After=network.target nss-lookup.target backend.service backup.service watch-config.service

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
"""

    create_service(service_name, service_file_content)
