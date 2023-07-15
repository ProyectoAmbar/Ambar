import certifi
import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

from controllers.productoController import ProductoController
from controllers.formularioAlquilerController import formularioAlquilerController
from controllers.TareaController import tareaController
from controllers.formMedidasController import fomMedidasController
from controllers.tareaModistaController import tareaModisteriaController

app = Flask(__name__)
cors = CORS(app)
product = ProductoController()
formAlquiler = formularioAlquilerController()
tareasController = tareaController()
formMedidas = fomMedidasController()
tareaModista = tareaModisteriaController()



#-----------------RUTAS DE PRODUCTOS-----------------#
@app.route('/productos' , methods=['POST'])
def crearProducto():
    data = request.get_json()
    json = product.create(data)
    print(json)
    return jsonify(json)

@app.route('/productos/<string:id>' , methods=['PUT'])
def actualizarProducto(id):
    data = request.get_json()
    json = product.updateProduct(id,data)
    return jsonify(json)

@app.route('/productos' , methods=['GET'])
def getAllProducto():
    json = product.getAllProducts()
    return jsonify(json)

@app.route('/productos/<string:id>', methods = ['GET'])
def getById(id):
    json = product.getById(id)
    print(json)
    return jsonify(json)

@app.route('/productos/getReferencia/<int:referencia>', methods=['GET'])
def getByReferencia(referencia):
    print(type(int(referencia)))
    json = product.getByRef(referencia)
    return jsonify(json)
@app.route('/productos/<string:id>',methods = ['DELETE'])
def Delete(id):
    json = product.deleteProducto(id)
    return jsonify(json)

###----------formulario alquiler----------------##

@app.route('/alquiler',methods=['POST'])
def CreateFormularioAlquiler():
    data = request.get_json()
    json = formAlquiler.create(data)
    return jsonify(json)

@app.route('/alquiler/<string:id>', methods = ['GET'])
def getFormatoAlquilerById(id):
    json = formAlquiler.getFormulariosAlquilerById(id)
    return jsonify(json)

@app.route('/alquiler',methods=['GET'])
def getAllFormatosAlquiler():
    json = formAlquiler.getAllFormularios()
    return jsonify(json)

@app.route('/alquiler/<string:id>', methods = ['PUT'])
def updateFormularioAlquiler(id):
    data = request.get_json()
    json = formAlquiler.UpdateFormularioAlquiler(id, data)
    return jsonify(json)
@app.route('/alquiler/<string:id>', methods = ['DELETE'])
def DeleteAlquiler(id):
    json = formAlquiler.Delete(id)
    return jsonify(json)


###------------tareas---------------###


@app.route('/tarea', methods=['POST'])
def CreateTarea():
    infoTarea = request.get_json()
    json = tareasController.Create(infoTarea)
    return jsonify(json)

@app.route('/tarea/<string:id>', methods=['GET'])
def getTareaById(id):
    json = tareasController.getById(id)
    return jsonify(json)

@app.route('/tarea')
def getAllTareas():
    json = tareasController.getAllTareas()
    return jsonify(json)

@app.route('/tarea/<string:id>', methods=['PUT'])
def updateTarea(id):
    data = request.get_json()
    json = tareasController.Update(id, data)
    return jsonify(json)

@app.route('/tarea/<string:id>', methods=['DELETE'])
def DeleteTarea(id):
    json = tareasController.Delete(id)
    return jsonify(json)

@app.route('/tarea/answer/<string:id>',methods=['PUT'])
def responderTarea(id):
    data = request.get_json()
    json = tareasController.responderTareaC(id, data, data['estado'])
    return jsonify(json)

@app.route('/tarea/verPendientes/<string:idEmpleado>',methods=['GET'])
def verTareasPendientes(idEmpleado):
    json = tareasController.verTareasPendientes(idEmpleado)
    return jsonify(json)

###------------FOMRATO MEDIDAS---------------##
@app.route('/formMedidas',methods=['POST'])
def crearFormMedidas():
    data = request.get_json()
    json = formMedidas.create(data)
    return jsonify(json)

@app.route('/formMedidas',methods=['GET'])
def getAllFormMedidas():
    json = formMedidas.getAll()
    return jsonify(json)

@app.route('/formMedidas/<string:id>', methods=['GET'])
def getFormMedidasById(id):
    json = formMedidas.getById(id)
    return jsonify(json)

@app.route('/formMedidas/<string:id>',methods=['PUT'])
def updateFormMedidas(id):
    data = request.get_json()
    json = formMedidas.UpdateForm(id,data)
    return jsonify(json)

@app.route('/formMedidas/<string:id>',methods=['DELETE'])
def deleteFormMedidas(id):
    json = formMedidas.deleteForm(id)
    return jsonify(json)

@app.route('/formMedidas/responder/<string:id>',methods=['PUT'])
def responderFormMedidas(id):
    data = request.get_json()
    json = formMedidas.responderFormMedidas(id, data)
    return jsonify(json)

###------------Tarea Modisteria---------------##
@app.route('/tareaModista',methods=['POST'])
def createTareaModista():
    data = request.get_json()
    json = tareaModista.Create(data)
    return jsonify(json)

@app.route('/tareaModista',methods=['GET'])
def getAllTareaModista():
    json = tareaModista.getAllTareaModista()
    return jsonify(json)

@app.route('/tareaModista/<string:id>',methods=['GET'])
def getTareaModistaById(id):
    json = tareaModista.getTareaModistaById(id)
    return jsonify(json)

@app.route('/tareaModista/<string:id>',methods=['PUT'])
def updateTareaModista(id):
    data = request.get_json()
    json = tareaModista.updateTareaModista(id,data)
    return jsonify(json)

@app.route('/tareaModista/<string:id>',methods=['DELETE'])
def deleteTareaModista(id):
    json = tareaModista.deleteTareaModista(id)
    return jsonify(json)

@app.route('/tareaModista/asignar/<string:id>',methods=['PUT'])
def asignarModista(id):
    data = request.get_json()
    json = tareaModista.AsignarTareaModista(id,data)
    return jsonify(json)

@app.route('/tareaModista/responder/<string:id>',methods=['PUT'])
def responderTareaModista(id):
    data = request.get_json()
    json = tareaModista.responderTareaModista(id,data)
    return jsonify(json)

@app.route('/tareaModista/sinasignar',methods=['GET'])
def getTareaModistaSinAsignar():
    json = tareaModista.getTareaModistaSinAsignar()
    return jsonify(json)

@app.route('/tareaModista/pendientes/<string:idModista>',methods=['GET'])
def getTareasModistaPendiente(idModista):
    json = tareaModista.getTareaModistaPendiente(idModista)
    return jsonify(json)


# -----------CONFIG AND MAIN ROOT-----------#
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


@app.route('/', methods=['GET'])
def test():
    json = {
        "message": "server is running",
        "port": 5000
    }
    return jsonify(json)


if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running: " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig['port']))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
    print("asdfasdf")
