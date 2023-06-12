from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import datetime
import requests
import re

from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


dataConfig = loadFileConfig()
app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"] = dataConfig["key"]
jwt = JWTManager(app)


@app.route("/login", methods=['POST'])
def createToken():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-users"] + '/user/validar'
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        user = response.json()

        expires = datetime.timedelta(seconds=60 * 60 * 24)
        token = create_access_token(identity=user, expires_delta=expires)
        return jsonify({
            "accesToken": token,
            "userId": user["_id"],
            "rol": user["rol"]["_id"]
        })
    else:
        json = []
        json.append({"message": "Por favor revise sus credenciales"})
        json.append(response.json())

        return jsonify(json)


if __name__ == '__main__':
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
