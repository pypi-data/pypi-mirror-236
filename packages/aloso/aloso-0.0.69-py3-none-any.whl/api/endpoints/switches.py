import json

from fastapi import APIRouter, Response

from api.server.commons import response_personalized
from output.shell.switch_shell import SwitchShell

router = APIRouter(
    prefix="/switches",
    tags=["Switches"],
)


@router.post("/")
async def save_all_configs():
    switch = SwitchShell()
    if switch.versioning_configs_from_ftp():
        response_personalized(message="Sauvegarde des switchs terminée !")

        return response_personalized(message="Une erreur est survenue lors de la sauvegarde des switchs",
                                     type_response="Fail")


@router.get("/ports")
async def get_switches_ports():
    data = {
        "switch 1": [33633],
        "switch 2": [18790],
        "switch 3": [56734],
        "switch 4": [9629, 20054],
        "switch 5": [27512],
        "switch 6": [51796],
        "switch 7": [20534, 51778],
        "switch 8": [17851, 40008],
        "switch 9": [9929, 20013, 32343],
        "switch 10": [53045],
        "switch 11": [43939],
        "switch 12": [18391],
        "switch 13": [36294, 3221, 50060],
        "switch 14": [38323],
        "switch 15": [23763],
        "switch 16": [22811, 49278],
        "switch 17": [39553, 34806],
        "switch 18": [28403],
        "switch 19": [34750, 54928],
        "switch 20": [50653],
        "switch 21": [14154, 37329],
        "switch 22": [35260, 41290, 14642],
        "switch 23": [5135],
        "switch 24": [32929],
        "switch 25": [428, 36239],
        "switch 26": [7217],
        "switch 27": [60997],
        "switch 28": [55211, 3917],
        "switch 29": [35345],
        "switch 30": [61070, 401],
        "switch 31": [37594],
        "switch 32": [14677, 23381],
        "switch 33": [35137],
        "switch 34": [63360, 50807],
        "switch 35": [60913, 30254],
        "switch 36": [25022],
        "switch 37": [49270, 5860],
        "switch 38": [19590, 23711],
        "switch 39": [20054],
        "switch 40": [20013]
    }

    return data
