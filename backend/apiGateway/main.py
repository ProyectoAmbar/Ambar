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
    excludedRoutes = ["/login","/logout","/productos/getAll","/productos/getById/?","/productos/getByReferencia/?","/user/create", "/estadoProducto/?", "/empleado", "/makeup/factura/?"]

    if excludedRoutes.__contains__(endPoint) :
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        print(usuario)
        if usuario['rol']['_id'] == '648f6d5104e7df55bd457ccd':
            pass
        elif usuario["rol"] is not None:
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

@app.route("/user/create/<string:id>",methods=['POST'])
def createUserWithRol(id):
    print("create user with rol")
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-users"] + '/user/rol/'+id, json=data,headers={"Content-Type": "application/json; charset=utf-8"})
    print(response.json())
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

@app.route('/PermisosRol',methods=['GET'])
def getAllPermisosRoles():
    response = requests.get(url=dataConfig["url-backend-users"]+'/PermisosRol', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())
@app.route('/PermisosRol/<string:id>',methods=['GET'])
def getPermisosRolById(id):
    response = requests.get(url=dataConfig["url-backend-users"]+'/PermisosRol/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/PermisosRol/permiso/<string:idPermiso>/rol/<string:idRol>')
def createPermisosRol(idPermiso, idRol):
    response = requests.post(url=dataConfig["url-backend-users"]+'/PermisosRol/permiso/'+idPermiso+'/rol/'+idRol, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/PermisosRol/<string:id>/permiso/<string:idPermiso>/rol/<string:rol>',methods=['PUT'])
def updatePermisosRol(id, idPermiso,rol):
    response = requests.put(url=dataConfig["url-backend-users"]+'/PermisosRol/'+id+'/permiso/'+idPermiso+'/rol/'+rol, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/PermisosRol/<string:id>',methods=['DELETE'])
def deletePermisosRol(id):
    response = requests.delete(url=dataConfig["url-backend-users"]+'/PermisosRol/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())
###--------------RUTAS DE EMPLEADOS--------------###

@app.route('/empleado',methods=['POST'])
def createEmpleado():
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-users"]+'/empleado', json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/empleado',methods=['GET'])
def getAllEmpleado():
    response = requests.get(url=dataConfig["url-backend-users"]+'/empleado', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/empleado/rol/<string:idRol>',methods=['POST'])
def createEmpleadoWithRol(idRol):
    data = request.get_json()
    rol = requests.get(url=dataConfig["url-backend-users"]+'/rol/'+idRol, headers={"Content-Type": "application/json; charset=utf-8"})
    if(rol.json() != None):
        response = requests.post(url=dataConfig["url-backend-users"]+'/empleado/rol/'+idRol,    json=data, headers={"Content-Type": "application/json; charset=utf-8"})
        return jsonify(response.json())
    else:
        return {"status": 400, "code": False, "message": "no se encontro el rol a asígnar, por favor ingrese correctamente el id"}

@app.route('/empleado/<string:id>',methods=['GET'])
def getEmpleadoById(id):
    response = requests.get(url=dataConfig["url-backend-users"]+'/empleado/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/empleado/<string:id>',methods=['PUT'])
def updateEmpleado(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-users"]+'/empleado/'+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/empleado/<string:id>',methods=['DELETE'])
def deleteEmpleado(id):
    response = requests.delete(url=dataConfig["url-backend-users"]+'/empleado/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


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
    print("crear productos")
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-productos"]+"/productos",json = data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/<string:id>', methods=['PUT'])
def uptadeProductos(id):
    print("update productos")
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+"/productos/"+id,json = data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/<string:id>',methods=['DELETE'])
def deleteProducto(id):
    print("delete Productos")
    response = requests.delete(url=dataConfig["url-backend-productos"]+"/productos/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/getReferencia/<string:referencia>',methods=['GET'])
def getByReferencia(referencia):
    print("get Productos By Referencia")
    response = requests.get(url=dataConfig["url-backend-productos"]+"/productos/getReferencia/"+referencia, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/bloquear/<string:id>',methods=['PUT'])
def bloquear(id):
    response = requests.put(url=dataConfig["url-backend-productos"]+"/productos/bloquear/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/productos/desbloquear/<string:id>',methods=['PUT'])
def desbloquear(id):
    response = requests.put(url=dataConfig["url-backend-productos"] + "/productos/desbloquear/" + id,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())



###--------------RUTAS DE FOMULARIO ALQUILER--------------###
@app.route('/alquiler',methods=['POST'])
def CreateFormularioAlquiler():
    print("crear formulario de alquiler")
    data = request.get_json()
    print(data['NumeroDeFactura'])
    form = requests.get(url=dataConfig["url-backend-productos"]+"/alquiler/factura/"+ data['NumeroDeFactura'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
    producto = requests.get(url=dataConfig["url-backend-productos"]+"/productos/"+data['idProducto'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
    try:
        if asesor['id'] and producto['_id'] and producto['disponible'] is True and form['status'] is False:
            alquiler = requests.post(url=dataConfig["url-backend-productos"]+"/alquiler", json=data, headers={"Content-Type": "application/json; charset=utf-8"})
            rtaAlquiler = alquiler.json()
            if rtaAlquiler.__len__() == 3:
                bloquear = requests.put(
                    url=dataConfig["url-backend-productos"] + "/productos/bloquear/" + data['idProducto'],
                    headers={"Content-Type": "application/json; charset=utf-8"})
                return jsonify(alquiler.json())
            else:
                return {"status": False, "Code": 400, "message": "No se ha podido crear el formulario de alquiler"}
        else:
            return {"status": False, "Code": 400, "message": "El producto se encuentra bloqueado"}
    except:
        return {"status": False, "Code": 400, "message": "no se encontro el asesor, producto, o ya existe ese numero de factura"}

@app.route('/alquiler',methods=['GET'])
def GetAllFormularioAlquiler():
    print("get all formulario de alquiler")
    response = requests.get(url=dataConfig['url-backend-productos']+"/alquiler",headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/alquiler/<string:id>',methods=['GET'])
def getFormularioAlquilerById(id):
    print("get by id formulario de alquiler")
    response = requests.get(url=dataConfig['url-backend-productos']+"/alquiler/"+id ,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/alquiler/<string:id>',methods=['PUT'])
def updateFormularioAlquiler(id):
    print("update formulario de alquiler")
    data = request.get_json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'], headers={"Content-Type": "application/json; charset=utf-8"})
    producto = requests.get(url=dataConfig["url-backend-productos"] + "/productos/" + data['idProducto'], headers={"Content-Type": "application/json; charset=utf-8"})
    print(producto.json())
    productoJson = producto.json()

    asesorJson = asesor.json()

    if asesorJson['id'] and productoJson[0]['_id']:
        response = requests.put(url=dataConfig['url-backend-productos']+"/alquiler/"+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
        return jsonify(response.json())
    else:
        return {"status": False, "Code": 400, "message": "no se encontro el cliente, el asesor o producto"}

@app.route('/alquiler/<string:id>',methods=['DELETE'])
def deleteFormularioAlquiler(id):
    print("delete formulario de alquiler")
    response = requests.delete(url=dataConfig['url-backend-productos']+"/alquiler/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


###--------------RUTAS DE TAREAS--------------###
@app.route('/tarea',methods=['GET'])
def GetAllTareas():
    print("get all tareas de asesor")
    response = requests.get(url=dataConfig['url-backend-productos']+"/tarea", headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea/<string:id>',methods=['GET'])
def GetTareaById(id):
    print("get all tareas de asesor")
    response = requests.get(url=dataConfig['url-backend-productos']+"/tarea/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea',methods=['POST'])
def CreateTarea():
    print("crear tarea de asesor")
    dict = []
    empleadoBool = False
    data = request.get_json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['idAsesor'],headers={"Content-Type": "application/json; charset=utf-8"})
    asesorJson = asesor.json()
    producto = requests.get(url=dataConfig["url-backend-productos"] + "/productos/" + data['idProducto'],headers={"Content-Type": "application/json; charset=utf-8"})
    productoJson = producto.json()
    if asesorJson['id'] and productoJson[0]['_id'] and empleadoBool:
        response = requests.post(url=dataConfig["url-backend-productos"] + "/tarea", json=data,headers={"Content-Type": "application/json; charset=utf-8"})
        dict.append(response.json())
        dict.append(asesorJson)
        dict.append(productoJson)
        return jsonify(dict)
    else:
        return {"status": False, "Code": 400, "message": "no se encontro el empleado, el asesor o producto"}

@app.route('/tarea/<string:id>', methods=['DELETE'])
def deleteTarea(id):
    print("delete TArea de asesor")
    response = requests.delete(url=dataConfig["url-backend-productos"] + "/tarea/"+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea/answer/<string:id>',methods=['PUT'])
def responderTarea(id):
    print("responder tarea de asesor")
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"] + "/tarea/answer/"+id,json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tarea/verPendientes/<string:idEmpleado>',methods=['GET'])
def verTareasPendientes(idEmpleado):
    print("ver Tareas pendientes")
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tarea/verPendientes/" + idEmpleado, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

###--------------RUTAS FORMULARIO DE MEDIDAS--------------###

@app.route('/formMedidas',methods=['POST'])
def crearFormMedidas():
    print("crear fomulario de medidas")
    data = request.get_json()
    formulario = requests.get(url=dataConfig['url-backend-productos']+"/alquiler/"+ data['formulario'] ,headers={"Content-Type": "application/json; charset=utf-8"}).json()
    asesor = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['asesor'],headers={"Content-Type": "application/json; charset=utf-8"}).json()
    producto = requests.get(url=dataConfig["url-backend-productos"]+"/productos/"+data['producto'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
    if (formulario['status'] and asesor['status'] and producto['status']):
        response = requests.post(url=dataConfig["url-backend-productos"] +'/formMedidas',json=data,headers={"Content-Type": "application/json; charset=utf-8"})
        return jsonify(response.json())
    else:
        return {"status":False, "code":400, "message":"no se encontro, el formulario, el asesor, o el producto"}

@app.route('/formMedidas',methods=['GET'])
def getAllFormMedidas():
    print("get all formulario de medidas")
    response = requests.get(url=dataConfig["url-backend-productos"] +'/formMedidas',headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/formMedidas/<string:id>',methods=['GET'])
def getFormMedidasById(id):
    print("get by id formulario de medidas")
    response = requests.get(url=dataConfig["url-backend-productos"] +'/formMedidas/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/formMedidas/<string:id>',methods=['PUT'])
def updateFormularioMedidas(id):
    data = request.get_json()
    response  = requests.put(url=dataConfig["url-backend-productos"] +'/formMedidas/'+id,json=data,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/formMedidas/<string:id>',methods=['DELETE'])
def deleteFormularioMedidas(id):
    response = requests.delete(url=dataConfig["url-backend-productos"] +'/formMedidas/'+id,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/formMedidas/responder/<string:id>', methods=['PUT'])
def responderFormMedidas(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"] +'/formMedidas/responder/'+id,json = data,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())



###--------------RUTAS FORMULARIO DE MEDIDAS--------------###
@app.route('/tareaModista',methods=['POST'])
def createTareaModista():
    data = request.get_json()
    formMedidas = requests.get(url=dataConfig['url-backend-productos'] + "/formMedidas/" + data['formMedidas'],
                              headers={"Content-Type": "application/json; charset=utf-8"}).json()
    modista = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['modista'],
                          headers={"Content-Type": "application/json; charset=utf-8"}).json()
    producto = requests.get(url=dataConfig["url-backend-productos"] + "/productos/" + data['producto'],
                            headers={"Content-Type": "application/json; charset=utf-8"}).json()
    try:
        if (formMedidas['_id'] and modista['id'] and producto['_id']):
            response = requests.post(url=dataConfig['url-backend-productos']+'/tareaModista', json = data, headers={"Content-Type": "application/json; charset=utf-8"})
            return jsonify(response.json())
    except:
        return {"status": False, "code":400, "message": "No se encontro el formMedidas, el modista o el producto"}

@app.route('/tareaModista',methods=['GET'])
def getAllTareaModista():
    response = requests.get(url=dataConfig['url-backend-productos']+'/tareaModista', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tareaModista/<string:id>',methods=['GET'])
def getTareaModistaById(id):
    response = requests.get(url=dataConfig['url-backend-productos']+'/tareaModista/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tareaModista/<string:id>',methods=['PUT'])
def updateTareaModista(id):
    data = request.get_json()
    formMedidas = requests.get(url=dataConfig['url-backend-productos'] + "/formMedidas/" + data['formMedidas'],
                              headers={"Content-Type": "application/json; charset=utf-8"}).json()
    modista = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['modista'],
                           headers={"Content-Type": "application/json; charset=utf-8"}).json()
    producto = requests.get(url=dataConfig["url-backend-productos"] + "/productos/" + data['producto'],
                            headers={"Content-Type": "application/json; charset=utf-8"}).json()
    try:
        if (formMedidas['_id'] and modista['id'] and producto['_id']):
            response = requests.put(url=dataConfig['url-backend-productos']+'/tareaModista/'+id, json = data,headers={"Content-Type": "application/json; charset=utf-8"})
            return jsonify(response.json())
    except:
        return {"status": False, "code":400, "message": "No se encontro el formMedidas, el modista o el producto"}

@app.route('/tareaModista/<string:id>',methods=['DELETE'])
def deleteTareaModista(id):
    response = requests.delete(url=dataConfig['url-backend-productos']+'/tareaModista/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return  jsonify(response.json())

@app.route('/tareaModista/sinAsignar',methods=['GET'])
def GetTareaModistaSinAsignar():
    response = requests.get(url=dataConfig['url-backend-productos']+'/tareaModista/sinAsignar', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/tareaModista/asignar/<string:id>',methods=['PUT'])
def asignarModista(id):
    data = request.get_json()
    modista = requests.get(url=dataConfig["url-backend-users"] + '/empleado/' + data['modista'],
                           headers={"Content-Type": "application/json; charset=utf-8"}).json()
    try:
        if modista['id']:
            response = requests.put(url=dataConfig["url-backend-productos"] + '/tareaModista/asignar/'+id, json = data, headers={"Content-Type": "application/json; charset=utf-8"})
            return jsonify(response.json())
    except:
        return {"status": False, "code": 400, "message": "No fue posible encontrar el modista"}

@app.route('/tareaModista/responder/<string:id>',methods=['PUT'])
def responderTareaModisteria(id):
    if verify_jwt_in_request():
        usuario = get_jwt_identity()
        print(usuario)
        empleado = requests.get(url=dataConfig['url-backend-users']+'/empleado/getByUser/'+usuario['_id']).json()
        tarea = requests.get(url=dataConfig["url-backend-productos"] + '/tareaModista/' + id, headers={"Content-Type": "application/json; charset=utf-8"}).json()
        if tarea['modista'] == "DBRef('empleado', ObjectId('"+empleado['id']+"'))":
            data = request.get_json()
            response = requests.put(url=dataConfig["url-backend-productos"] + '/tareaModista/responder/' + id, json=data,headers={"Content-Type": "application/json; charset=utf-8"})
            return jsonify(response.json())
        else:
            return {"status": False, "code": 400, "message": "No es el modista asignado para esta tarea"}

@app.route('/tareaModista/pendientes/<string:idModista>',methods=['GET'])
def getTareasPendientes(idModista):
    response = requests.get(url=dataConfig["url-backend-productos"] +'/tareaModista/pendientes/'+idModista, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

#-----------TareaLavanderia-----------#
@app.route('/lavanderia',methods=['POST'])
def createTareaLavanderia():
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-productos"]+'/lavanderia',json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia',methods=['GET'])
def getAllTareaLavanderia():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/lavanderia', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/<string:id>',methods=['GET'])
def getTareaLavanderiaByid(id):
    response = requests.get(url=dataConfig["url-backend-productos"]+'/lavanderia/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/sinAsignar',methods=['GET'])
def getTareaLavanderiaSinAsignar():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/lavanderia/sinAsignar', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/pendientes',methods=['GET'])
def getTareaLavanderiaPendientes():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/lavanderia/pendientes', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/pendientes/<string:id>',methods=['GET'])
def getTareaLavanderiaPendienteByEmpleado(id):
    response = requests.get(url=dataConfig["url-backend-productos"]+'/lavanderia/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/<string:id>',methods=['PUT'])
def updateTareaLavanderia(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+'/lavanderia/'+id,json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/<string:id>',methods=['DELETE'])
def deleteTareaLavanderia(id):
    response = requests.delete(url=dataConfig["url-backend-productos"]+'/lavanderia/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/lavanderia/answer/<string:id>',methods=['PUT'])
def responderTareaLavanderia(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+'/lavanderia/answer/'+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())
@app.route('/lavanderia/<string:id>/empleado/<string:idLavanderia>',methods=['PUT'])
def asignarLavanderia(id, idLavanderia):
    tarea = requests.get(url=dataConfig['url-backend-productos'] + '/lavanderia/'+id).json()
    empleado = requests.get(url=dataConfig['url-backend-users'] + '/empleado/'+idLavanderia).json()
    try:
        if tarea['_id'] and empleado['id']:
            response = requests.put(url=dataConfig["url-backend-productos"]+'/lavanderia/'+id+'/empleado/'+idLavanderia, headers={"Content-Type": "application/json; charset=utf-8"})
            return jsonify(response.json())
    except:
        return {"status": False, "code": 400, "message": "no se encontro la tarea o el empleado"}


#----------ENTREGA-DEVOLUCION----------#

@app.route('/entregaDevolucion',methods=['POST'])
def createEntregaDevolucion():
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-productos"]+'/entregaDevolucion',json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/entregaDevolucion',methods=['GET'])
def getAllEntregaDevolucion():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/entregaDevolucion', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/entregaDevolucion/<string:id>',methods=['GET'])
def getEntregaDevolucionByid(id):
    response = requests.get(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


@app.route('/entregaDevolucion/<string:id>',methods=['PUT'])
def updateEntregaDevolucion(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/'+id,json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/entregaDevolucion/<string:id>',methods=['DELETE'])
def deleteEntregaDevolucion(id):
    response = requests.delete(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/'+id, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


@app.route('/entregaDevolucion/SinEntregar',methods=['GET'])
def getEntregaDevolucionSinAsignar():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/SinEntregar', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/entregaDevolucion/SinDevolver',methods=['GET'])
def getEntregaDevolucionPendientes():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/SinDevolver', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/entregaDevolucion/entrega/<string:id>',methods=['PUT'])
def responderEntrega(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/entrega/'+id, json=data,headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())


@app.route('/entregaDevolucion/devolucion/<string:id>',methods=['PUT'])
def responderDevolucion(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"]+'/entregaDevolucion/devolucion/'+id, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/calendar',methods=['GET'])
def calendarioAdmin():
    response = requests.get(url=dataConfig["url-backend-productos"]+'/calendar', headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/calendar/<string:idAsesor>',methods=['GET'])
def calendarioAdminViewAsesor(idAsesor):
    response = requests.get(url=dataConfig["url-backend-productos"]+'/calendar/'+idAsesor, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/estadoProducto/<string:factura>',methods=['GET'])
def getEstadoProducto(factura):
    dict = []
    formulario = requests.get(url=dataConfig['url-backend-productos']+'/alquiler/factura/'+ factura, headers={"Content-Type": "application/json; charset=utf-8"}).json()
    dict.append(formulario)
    try:
        tarea = requests.get(url=dataConfig['url-backend-productos']+'/tarea/formulario/'+ formulario['_id'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
        tareaModisteria = requests.get(url=dataConfig['url-backend-productos']+'/tareaModista/formulario/'+formulario['_id'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
        lavanderia = requests.get(url=dataConfig['url-backend-productos']+'/lavanderia/formulario/'+ formulario['_id'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
        entregaDevolucion = requests.get(url=dataConfig['url-backend-productos']+'/entregaDevolucion/formulario/'+ formulario['_id'], headers={"Content-Type": "application/json; charset=utf-8"}).json()
        dict.append(tarea)
        dict.append(tareaModisteria)
        dict.append(lavanderia)
        dict.append(entregaDevolucion)
        return jsonify(dict)
    except:
        return {"message": "no se encontro el formulario con numero de factura: "+factura}


#------------- CAJA -----------#
@app.route('/caja/agregar', methods=['PUT'])
def agregarCaja():
    data = request.get_json()
    response = requests.put(url=dataConfig['url-backend-productos']+'/caja/agregar',json= data, headers={"Content-Type": "application/json; charset=utf-8"}).json()
    return jsonify(response)

@app.route('/caja/retirar', methods=['PUT'])
def retirarCaja():
    data = request.get_json()
    response = requests.put(url=dataConfig['url-backend-productos']+'/caja/retirar',json= data, headers={"Content-Type": "application/json; charset=utf-8"}).json()
    return jsonify(response)

@app.route('/caja/saldo', methods=['GET'])
def getSaldo():
    response = requests.get(url=dataConfig['url-backend-productos']+'/caja/saldo', headers={"Content-Type": "application/json; charset=utf-8"}).json()
    return jsonify(response)

@app.route('/caja/restaurar', methods=['GET'])
def restaurarSaldo():
    response = requests.put(url=dataConfig['url-backend-productos'] + '/caja/restaurar',headers={"Content-Type": "application/json; charset=utf-8"}).json()
    return jsonify(response)

## ----------- FORMULARIO MAKEUP -----------##

@app.route('/makeup',methods=['POST'])
def createFormMakeup():
    data = request.get_json()
    response = requests.post(url=dataConfig["url-backend-productos"]+'/makeup',json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    return jsonify(response.json())

@app.route('/makeup', methods=['GET'])
def getAllFormMakeup():
    response = requests.get(url=dataConfig["url-backend-productos"]+"/makeup",headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/makeup/<string:id>', methods=['GET'])
def getAllFormMakeupById(id):
    response = requests.get(url=dataConfig["url-backend-productos"] + "/makeup/"+id,headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/makeup/factura/<string:factura>', methods=['GET'])
def getFormMakeUpByFactura(factura):
    response = requests.get(url=dataConfig["url-backend-productos"] + "/makeup/factura/" + factura,headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)
@app.route('/makeup/<string:id>', methods=['DELETE'])
def deleteFormMakeUpById(id):
    response = requests.delete(url=dataConfig["url-backend-productos"] + "/makeup/" + id,headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/makeup/<string:id>', methods=['PUT'])
def updateFormMakeUpById(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"] + "/makeup/" + id, json=data, headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/makeup/dia', methods=['GET'])
def getFormMakeUpByDia():
    data = request.get_json()
    response = requests.get(url=dataConfig["url-backend-productos"] + "/makeup/dia", json=data, headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)


## ----------- FORMULARIO TAREAS MAKEUP -----------##
@app.route('/tareaMakeup', methods=['POST'])
def createTareaMakeup():
    data = request.get_json()
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tareaMakeup",json=data, headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/tareaMakeup', methods=['GET'])
def getTareaMakeup():
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tareaMakeup",headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/tareaMakeup/<string:id>', methods=['GET'])
def getTareaMakeupById(id):
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tareaMakeup/"+id, headers={"Content-Type": "application/json; charset=utf8"})
    return jsonify(response)

@app.route('/tareaMakeup/<string:id>', methods=['UPDATE'])
def updateTareaMakeup(id):
    data = request.get_json()
    response = requests.put(url=dataConfig["url-backend-productos"] + "/tareaMakeup/"+id, json=data, headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/tareaMakeup/<string:id>', methods=['DELETE'])
def deleteTareaMakeup(id):
    response = requests.delete(url=dataConfig["url-backend-productos"] + "/tareaMakeup/"+id , headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/tareaMakeup/verPendientes/<string:id>', methods=['GET'])
def GetAllPendientesTareaMakeupByStylist(id):
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tareaMakeup/verPendientes/"+ id, headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)

@app.route('/tareaMakeup/verPendientes', methods=['GET'])
def GetAllPendientesTareaMakeup():
    response = requests.get(url=dataConfig["url-backend-productos"] + "/tareaMakeup/verPendientes", headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)
@app.route('/tareaMakeup/responder/<string:id>', methods=['PUT'])
def responderTareaMakeup(id):
    response = requests.put(url=dataConfig["url-backend-productos"] + "/tareaMakeup/responder/"+id, headers={"Content-Type": "application/json; charset=utf8"}).json()
    return jsonify(response)


#-------------------------------------------------#


if __name__ == '__main__':
    print("Server running : " + "http://" + dataConfig["url-backend-productos"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
