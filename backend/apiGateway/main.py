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


###-------VALIDACIÓN DE PERMISOS-------###
@app.before_request
def before_request_callback():
    endPoint = limpiarURL(request.path)
    print(endPoint)
    excludedRoutes = ["/login","/logout","/productos/getAll","/productos/getById/?","/productos/getByReferencia/?","/user/create"]
    if excludedRoutes.__contains__(endPoint):
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
@app.route("/user/create", methods=['POST'])
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
    print(response)
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


###--------------RUTAS DE ROLES--------------###
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


###-------RUTAS PERMISOS-ROLES--------------###




###--------------RUTAS DE EMPLEADOS--------------###




###--------------RUTAS DE PRODUCTOS--------------###
@app.route('/productos/getAll',methods=['GET'])
def getAllProductos():
    print("get all productos")
    response = requests.get(url=dataConfig["url-backend-productos"]+"/productos", headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


@app.route('/productos/getById/<string:id>',methods=['GET'])
def getProductoById(id):
    print("get productos by id")
    response = requests.get(url=dataConfig["url-backend-productos"]+"/productos/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos',methods=['POST'])
def CreateProductos():
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-productos"]+"/productos",json = data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/<string:id>', methods=['PUT'])
def uptadeProductos(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+"/productos/"+id,json = data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/<string:id>',methods=['DELETE'])
def deleteProducto(id):
    response = requests.delete(url=dataConfig["url-backend-productos"]+"/productos/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/getReferencia/<string:referencia>')
def getByReferencia(referencia):
    response = requests.get(url=dataConfig["url-backend-productos"]+"/productos/getReferencia/"+referencia, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())
###--------------RUTAS DE FOMULARIO ALQUILER--------------###
@app.route('/alquiler',methods=['POST'])
def CreateFormularioAlquiler():
    data = request.get_json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'], headers={"Content-Type": "application/json; charset=utf-8"})
    cliente = requests.get(url=dataConfig["url-backend-users"]+'/user/'+data['idCliente'], headers={"Content-Type": "application/json; charset=utf-8"})
    producto = requests.get(url=dataConfig["url-backend-productos"]+"/productos/"+data['idProducto'], headers={"Content-Type": "application/json; charset=utf-8"})
    if asesor.status_code == 200 and cliente.status_code == 200 and producto.status_code == 200:
        alquiler = requests.post(url=dataConfig["url-backend-productos"]+"/alquiler", json=data, headers={"Content-Type": "application/json; charset=utf-8"})
        print(alquiler)
        return jsonify(alquiler.json())
    else:
        return {"status": False, "Code": 400, "message": "no se encontro el cliente, el asesor o producto"}

@app.route('/alquiler',methods=['GET'])
def GetAllFormularioAlquiler():
    response = requests.get(url=dataConfig['url-backend-productos']+"/alquiler",headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/alquiler/<string:id>',methods=['GET'])
def getFormularioAlquilerById(id):
    response = requests.get(url=dataConfig['url-backend-productos']+"/alquiler/"+id ,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/alquiler/<string:id>',methods=['PUT'])
def updateFormularioAlquiler(id):
    data = request.get_json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'], headers={"Content-Type": "application/json; charset=utf-8"})
    cliente = requests.get(url=dataConfig["url-backend-users"] + '/user/' + data['idCliente'], headers={"Content-Type": "application/json; charset=utf-8"})
    producto = requests.get(url=dataConfig["url-backend-productos"] + "/productos/" + data['idProducto'], headers={"Content-Type": "application/json; charset=utf-8"})
    print(producto.json())
    productoJson = producto.json()
    clienteJson = cliente.json()
    asesorJson = asesor.json()

    if clienteJson['_id'] and asesorJson['id'] and productoJson[0]['_id']:
        response = requests.put(url=dataConfig['url-backend-productos']+"/alquiler/"+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
        return jsonify(response.json())
    else:
        return {"status": False, "Code": 400, "message": "no se encontro el cliente, el asesor o producto"}

@app.route('/alquiler/<string:id>',methods=['DELETE'])
def deleteFormularioAlquiler(id):
    response = requests.delete(url=dataConfig['url-backend-productos']+"/alquiler/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


###--------------RUTAS DE TAREAS--------------###
@app.route('/tarea',methods=['GET'])
def GetAllTareas():
    response = requests.get(url=dataConfig['url-backend-productos']+"/tarea", headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea/<string:id>',methods=['GET'])
def GetTareaById(id):
    response = requests.get(url=dataConfig['url-backend-productos']+"/tarea/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea',methods=['POST'])
def CreateTarea():
    dict = []
    empleadoBool = True
    data = request.get_json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'],headers={"Content-Type": "application/json; charset=utf-8"})
    asesorJson = asesor.json()
    producto = requests.get(url=dataConfig["url-backend-productos"] + "/productos/" + data['idProducto'],headers={"Content-Type": "application/json; charset=utf-8"})
    productoJson = producto.json()
    if data['idEmpleado'] is not None:
        empleado = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idEmpleado'],headers={"Content-Type": "application/json; charset=utf-8"})
        if empleado.status_code != 200:
            empleadoBool = False
    if asesorJson['id'] and productoJson[0]['_id'] and empleadoBool:
        response = requests.post(url=dataConfig["url-backend-productos"] + "/tarea", json=data,headers={"Content-Type": "application/json; charset=utf-8"})
        dict.append(response.json())
        dict.append(asesorJson)
        dict.append(productoJson)
        if empleadoBool:
            dict.append(empleado.json())
        return jsonify(dict)
    else:
        return {"status": False, "Code": 400, "message": "no se encontro el empleado, el asesor o producto"}

@app.route('/tarea/<string:id>', methods=['DELETE'])
def deleteTarea(id):
    response = requests.delete(url=dataConfig["url-backend-productos"] + "/tarea/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea/answer/<string:id>',methods=['PUT'])
def responderTarea(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"] + "/tarea/answer/"+id,json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea/asignar/<string:id>',methods=['PUT'])
def asignarTarea(id):
    data = request.get_json()
    print(data['empleado'])
    empleado = requests.get(url = dataConfig["url-backend-users"]+"/empleado/"+data['empleado'],headers={"Content-Type": "application/json; charset=utf-8"})
    if empleado.status_code == 200:
        response = requests.put(url=dataConfig["url-backend-productos"] + "/tarea/asignar/" + id, json=data,headers={"Content-Type": "application/json; charset=utf-8"})
        return jsonify(response.json())
    else:
        return jsonify(empleado.json())


@app.route('/tarea/verPendientes/<string:idEmpleado>',methods=['GET'])
def verTareasPendientes(idEmpleado):
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tarea/verPendientes/" + idEmpleado, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())



















if __name__ == '__main__':
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
