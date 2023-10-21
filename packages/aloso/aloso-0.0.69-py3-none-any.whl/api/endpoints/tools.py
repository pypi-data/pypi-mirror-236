import json

from fastapi import APIRouter, Response

import config
from api.server.commons import response_personalized
from output.shell.configs_shell import ConfigsShell
from output.tools.grafana_shell import GrafanaShell
from production.configurations.config_files_data import syslog_ng, clients, count, top_top_errors, loki_conf, \
    loki_service, \
    promtail_conf, promtail_service, base, prometheus_conf, prometheus_service

router = APIRouter(
    prefix="/tools",
    tags=["Tools"],
)


# TODO: Add Prometheus to the list of tools
@router.post("/")
async def edit_local_param(data: dict):
    if not hasattr(edit_local_param, "configuration"):
        edit_local_param.configuration = ConfigsShell()
        edit_local_param.configuration.config_file_path = config.config_file

    sudo = data["useSudo"]
    tool = data["tool"]
    operation = data["operation"]
    input_values = data["inputValues"]

    tools_dict = {
        "connection": ["grafana_host", "grafana_port", "grafana_username"],
        "grafana": ["grafana_wget_url", "grafana_ini_file"],
        "loki": ["loki_wget_url", "loki_yaml_file", "loki_service_file"],
        "promtail": ["promtail_wget_url", "promtail_yaml_file", "promtail_service_file"]
    }

    tool_keys = tools_dict.get(tool, [])

    cleaned_input_values = {k: v for k, v in input_values.items() if k in tool_keys}
    cleaned_input_values["use_sudo"] = sudo

    tools = {
        "grafana": {"method": GrafanaShell().install_grafana, "success_message": "Grafana installé avec succès"},
        "loki": {"method": GrafanaShell().install_loki, "success_message": "Loki installé avec succès"},
        "promtail": {"method": GrafanaShell().install_promtail, "success_message": "Promtail installé avec succès"},
    }

    if operation == "install":
        if tool in tools:
            try:
                # TODO : Activate next line to install tools
                # tools[tool]["method"]()
                return response_personalized(message=tools[tool]["success_message"])
            except Exception as e:
                return response_personalized(message=f"Erreur lors de l'installation de {tool}: {e}",
                                             type_response="Fail")

        else:
            return response_personalized(message=f"Outil inconnu", type_response="Fail")

    elif operation == "save":
        try:
            for key, value in cleaned_input_values.items():
                edit_local_param.configuration.variable_name = key
                edit_local_param.configuration.variable_value = value
                # TODO : Activate next line to save configuration
                # edit_local_param.configuration.edit_variable()
                return response_personalized(message="Configuration sauvegardée")

        except Exception as e:
            return response_personalized(message=f"Erreur lors de la sauvegarde: {e}", type_response="Fail")

    else:
        return response_personalized(message="Opération inconnue", type_response="Fail")


@router.get("/")
async def get_tools():
    return {
        "host": config.grafana_host,
        "port": config.grafana_port,
        "user": config.grafana_username,
        "grafanaUrl": config.grafana_wget_url,
        "grafanaIni": config.grafana_ini_file,
        "lokiUrl": config.loki_wget_url,
        "lokiYaml": config.loki_yaml_file,
        "lokiService": config.loki_service_file,
        "promtailUrl": config.promtail_wget_url,
        "promtailYaml": config.promtail_yaml_file,
        "promtailService": config.promtail_service_file,
        "prometheusUrl": config.prometheus_wget_url,
        "prometheusYaml": config.prometheus_yaml_file,
        "prometheusService": config.prometheus_service_file,
        "syslog": syslog_ng,
        "base": base,
        "clients": clients,
        "count": count,
        "top": top_top_errors,
        "loki-yaml-content": loki_conf,
        "loki-service-content": loki_service,
        "promtail-yaml-content": promtail_conf,
        "promtail-service-content": promtail_service,
        "prometheus-yaml-content": prometheus_conf,
        "prometheus-service-content": prometheus_service,

    }
