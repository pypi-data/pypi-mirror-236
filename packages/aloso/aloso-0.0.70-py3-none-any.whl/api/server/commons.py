import json

from fastapi import Response


def response(class_type, operation, type_response="Success"):
    response_content = {"message": " Un problème est survenu lors de la " + operation + " de l' " + class_type}
    response_status = 500
    if type_response == "Success":
        response_content = {"message": "La " + operation + " de " + class_type + " a été effectuée avec succès"}
        response_status = 200
    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


def response_personalized(message="Opération effectuée avec succès !", type_response="Success"):
    if type_response == "Success":
        return Response(status_code=200, content=json.dumps({"message": message}), media_type="application/json")
    else:
        return Response(status_code=500, content=json.dumps({"message": message}), media_type="application/json")
