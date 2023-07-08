from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import datetime
import requests
import re

from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt, unset_jwt_cookies, set_access_cookies
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

@app.before_request
def before_request_callback():
    endPoint = limpiarURL(request.path)
    print(endPoint)
    excludedRoutes = ["/login",]
    if excludedRoutes.__contains__(request.path):
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        print(usuario)
        if usuario["rol"] is not None:
            tienePersmiso = validarPermiso(endPoint, request.method, usuario["rol"]["_id"])
            print(tienePersmiso)
            if not tienePersmiso:
                return jsonify({"message": "Permission denied"}), 401
        else:
            return jsonify({"message": "Permission denied"}), 401


def limpiarURL(url):
    print("valida url")
    partes = url.split("/")
    for laParte in partes:
        if re.search('\\d', laParte):
            url = url.replace(laParte, "?")
    return url


def validarPermiso(endPoint, metodo, idRol):
    print(metodo)
    url = dataConfig["url-backend-users"] + "/PermisosRol/validar-permiso/rol/" + str(idRol)
    tienePermiso = False
    headers = {"Content-Type": "application/json; charset=utf-8"}
    body = {
        "url": endPoint,
        "metodo": metodo
    }
    response = requests.get(url, json=body, headers=headers)

    try:
        data = response.json()
        if "_id" in data:
            tienePermiso = True
        else:
            tienePermiso = False
    except:
        pass
    return tienePermiso

# --------------RUTAS DE USUARIOS-------------- #
@app.route("/user", methods=['POST'])
def createUser():
    print("createUser")
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-users"]+'/user', json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/login", methods=['POST'])
def Login():
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


@app.route("/logout", methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    res = jsonify({
        "status": 200,
        "msg": "token successfully revoked"
    })
    unset_jwt_cookies(res)
    return res

@app.route("/user", methods=['GET'])
def getAllUser():
    print("getAllUser")
    response = requests.get(url=dataConfig["url-backend-users"]+'/user', headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/user/<string:id>", methods=['GET'])
def getUserById(id):
    print("getUserById")
    response = requests.get(url=dataConfig["url-backend-users"]+'/user/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/user/<string:id>", methods=['PUT'])
def updateUser(id):
    print("updateUser")
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-users"]+'/user/'+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/user/<string:userId>/rol/<string:rolId>", methods=['PUT'])
def assignRole(userId,rolId):
    print("assignRole")
    response = requests.put(url=dataConfig["url-backend-users"]+'/user/asignarRol/' + userId + '/rol/' + rolId, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/user/<string:id>", methods=['DELETE'])
def deleteUser(id):
    print("deleteuser")
    response = requests.delete(url=dataConfig["url-backend-users"] + '/user/' + id)
    response.json()
    print(response)
    return jsonify(response.json())


# --------------RUTAS DE ROLES-------------- #

@app.route("/rol", methods=['POST'])
def createRol():
    print("createRol")
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-users"]+'/rol', json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/rol", methods=['GET'])
def getAllRol():
    print("getAllUser")
    response = requests.get(url=dataConfig["url-backend-users"]+'/rol', headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/rol/<string:id>", methods=['GET'])
def getRolById(id):
    print("getRolById")
    response = requests.get(url=dataConfig["url-backend-users"]+'/rol/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())


@app.route("/rol/<string:id>", methods=['PUT'])
def updateRol(id):
    print("updateRol")
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-users"]+'/rol/'+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response)
    return jsonify(response.json())

@app.route("/rol/<string:id>", methods=['DELETE'])
def deleteRol(id):
    print("deleteRol")
    response = requests.delete(url=dataConfig["url-backend-users"] + '/rol/' + id)
    response.json()
    print(response)
    return jsonify(response.json())

#formulario
@app.route('/Alquiler',methods=['POST'])
def CreateFormularioAlquiler():
    data = request.get_json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'])
    cliente = requests.get(url=dataConfig["url-backend-users"]+'/user/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    clienteJson = cliente.json()
    asesorJson = asesor.json()
    if(clienteJson['correo'] and asesorJson['identificacion']):
        alquiler = request.post()








if __name__ == '__main__':
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
