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
from repositories.repositorioProductos import RepositorioProductos
from controllers.lavanderiaController import lavanderiaController
from controllers.entregaDevolucionController import entregaDevolucionController
from controllers.calendar import calendar
from controllers.cajaController import cajaController
from controllers.auditoriaController import auditoriaController
from controllers.makeupController import makeupController
from controllers.tareaMakeUpController import tareaMakeupController

from models.producto import Producto
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId

app = Flask(__name__)
cors = CORS(app)

product = ProductoController()
formAlquiler = formularioAlquilerController()
tareasController = tareaController()
formMedidas = fomMedidasController()
tareaModista = tareaModisteriaController()
tareaLavanderia = lavanderiaController()
entregaDevolver = entregaDevolucionController()
calendario = calendar()
caja = cajaController()
audit = auditoriaController()
makeup = makeupController()
tareaMake = tareaMakeupController()

scheduler = BackgroundScheduler()
scheduler.start()
repoDb = RepositorioProductos()


def desbloquearProducto(id, idTarea):
    print("disparo ;))")
    job = repoDb.getDb()['jobs']
    search = repoDb.getById(id)
    try:
        if search['disponible'] is False:
            productoUpdate = {
                "nombre": search['nombre'],
                "referencia": search['referencia'],
                "imagenProducto": search['imagenProducto'],
                "color": search['color'],
                "disponible": True
            }
            repoDb.update(id, Producto(productoUpdate))
        print(job.delete_one({'_id': ObjectId(idTarea)}).deleted_count)
    except:
        print(job.delete_one({'_id': ObjectId(idTarea)}).deleted_count)
        pass


db = repoDb.getDb()
tareas = db['jobs'].find()
for tarea in tareas:
    fun = globals()[tarea['fun']]
    if tarea['fecha'] <= str(datetime.now()):
        print("menor jaja lol")
        fun(tarea['producto'], tarea['_id'])
    else:
        item = {
            "fun": tarea['fun'],
            "trigger": tarea['trigger'],
            "fecha": tarea['fecha'],
            "producto": tarea['producto'],
            "creada": True
        }
        db['jobs'].update_one({'_id': ObjectId(tarea['_id'])}, {"$set": item})
        scheduler.add_job(fun, tarea['trigger'], next_run_time=tarea['fecha'], args=[tarea['producto'], tarea['_id']])


@app.before_request
def consultarEIniciarTareas():
    db = repoDb.getDb()
    tareas = db['jobs'].find()
    for tarea in tareas:
        fun = globals()[tarea['fun']]
        if tarea['fecha'] < str(datetime.now()):
            print("menor jaja lol")
            fun(tarea['producto'], tarea['_id'])
        elif tarea['creada'] is False:
            item = {
                "fun": tarea['fun'],
                "trigger": tarea['trigger'],
                "fecha": tarea['fecha'],
                "producto": tarea['producto'],
                "creada": True
            }
            db['jobs'].update_one({'_id': ObjectId(tarea['_id'])}, {"$set": item})
            scheduler.add_job(fun, tarea['trigger'], next_run_time=tarea['fecha'],
                              args=[tarea['producto'], tarea['_id']])


scheduler.add_job(consultarEIniciarTareas, 'interval', seconds=6)


# -----------------RUTAS DE PRODUCTOS-----------------#
@app.route('/productos', methods=['POST'])
def crearProducto():
    data = request.get_json()
    json = product.create(data)
    print(json)
    return jsonify(json)


@app.route('/productos/<string:id>', methods=['PUT'])
def actualizarProducto(id):
    data = request.get_json()
    json = product.updateProduct(id, data)
    return jsonify(json)


@app.route('/productos', methods=['GET'])
def getAllProducto():
    json = product.getAllProducts()
    return jsonify(json)


@app.route('/productos/<string:id>', methods=['GET'])
def getById(id):
    json = product.getById(id)
    print(json)
    return jsonify(json)


@app.route('/productos/bloquear/<string:id>', methods=['PUT'])
def bloquear(id):
    json = product.bloquearProducto(id)
    return jsonify(json)


@app.route('/productos/desbloquear/<string:id>', methods=['PUT'])
def desbloquear(id):
    json = product.desbloquearProducto(id)
    return jsonify(json)


@app.route('/productos/getReferencia/<int:referencia>', methods=['GET'])
def getByReferencia(referencia):
    print(type(int(referencia)))
    json = product.getByRef(referencia)
    return jsonify(json)


@app.route('/productos/<string:id>', methods=['DELETE'])
def Delete(id):
    json = product.deleteProducto(id)
    return jsonify(json)


###----------formulario alquiler----------------##

@app.route('/alquiler', methods=['POST'])
def CreateFormularioAlquiler():
    data = request.get_json()
    json = formAlquiler.create(data)
    return jsonify(json)


@app.route('/alquiler/<string:id>', methods=['GET'])
def getFormatoAlquilerById(id):
    json = formAlquiler.getFormulariosAlquilerById(id)
    return jsonify(json)


@app.route('/alquiler', methods=['GET'])
def getAllFormatosAlquiler():
    json = formAlquiler.getAllFormularios()
    return jsonify(json)


@app.route('/alquiler/<string:id>', methods=['PUT'])
def updateFormularioAlquiler(id):
    data = request.get_json()
    json = formAlquiler.UpdateFormularioAlquiler(id, data)
    return jsonify(json)


@app.route('/alquiler/<string:id>', methods=['DELETE'])
def DeleteAlquiler(id):
    json = formAlquiler.Delete(id)
    return jsonify(json)


@app.route('/alquiler/getEntregas', methods=['GET'])
def getEntregas():
    json = formAlquiler.getFormPorEntregar()
    return jsonify(json)


@app.route('/alquiler/factura/<string:factura>', methods=['GET'])
def getByFactura(factura):
    json = formAlquiler.getByFactura(factura)
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


@app.route('/tarea', methods=['GET'])
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


@app.route('/tarea/answer/<string:id>', methods=['PUT'])
def responderTarea(id):
    data = request.get_json()
    json = tareasController.responderTareaC(id, data)
    return jsonify(json)


@app.route('/tarea/verPendientes/<string:idEmpleado>', methods=['GET'])
def verTareasPendientes(idEmpleado):
    json = tareasController.verTareasPendientesPorAsesor(idEmpleado)
    return jsonify(json)

@app.route('/tarea/completed/<string:id>', methods=['GET'])
def getAllAsesorCompleted(id):
    response = tareasController.getTaskCompleted(id)
    return jsonify(response)

@app.route('/tarea/formulario/<string:formulario>')
def getByFormulario(formulario):
    json = tareasController.getByFormulario(formulario)
    return jsonify(json)


@app.route('/tarea/getAllPendientes', methods=['GET'])
def getAllPendientes():
    json = tareasController.getAllTareasPendientes()
    return jsonify(json)


###------------FOMRATO MEDIDAS---------------##
@app.route('/formMedidas', methods=['POST'])
def crearFormMedidas():
    data = request.get_json()
    json = formMedidas.create(data)
    return jsonify(json)


@app.route('/formMedidas', methods=['GET'])
def getAllFormMedidas():
    json = formMedidas.getAll()
    return jsonify(json)


@app.route('/formMedidas/<string:id>', methods=['GET'])
def getFormMedidasById(id):
    json = formMedidas.getById(id)
    return jsonify(json)


@app.route('/formMedidas/<string:id>', methods=['PUT'])
def updateFormMedidas(id):
    data = request.get_json()
    json = formMedidas.UpdateForm(id, data)
    return jsonify(json)


@app.route('/formMedidas/<string:id>', methods=['DELETE'])
def deleteFormMedidas(id):
    json = formMedidas.deleteForm(id)
    return jsonify(json)


@app.route('/formMedidas/responder/<string:id>', methods=['PUT'])
def responderFormMedidas(id):
    data = request.get_json()
    json = formMedidas.responderFormMedidas(id, data)
    return jsonify(json)


###------------Tarea Modisteria---------------##
@app.route('/tareaModista', methods=['POST'])
def createTareaModista():
    data = request.get_json()
    json = tareaModista.Create(data)
    return jsonify(json)


@app.route('/tareaModista', methods=['GET'])
def getAllTareaModista():
    json = tareaModista.getAllTareaModista()
    return jsonify(json)


@app.route('/tareaModista/<string:id>', methods=['GET'])
def getTareaModistaById(id):
    json = tareaModista.getTareaModistaById(id)
    return jsonify(json)

@app.route('/tareaModista/completed/<string:id>')
def getTareaModistaCompleted(id):
    json = tareaModista.getTaskCompleted(id)
    return jsonify(json)


@app.route('/tareaModista/formulario/<string:formulario>')
def getTareaModistaByFormulario(formulario):
    json = tareaModista.getTareaModisteriaByFormulario(formulario)
    return jsonify(json)


@app.route('/tareaModista/<string:id>', methods=['PUT'])
def updateTareaModista(id):
    data = request.get_json()
    json = tareaModista.updateTareaModista(id, data)
    return jsonify(json)


@app.route('/tareaModista/<string:id>', methods=['DELETE'])
def deleteTareaModista(id):
    json = tareaModista.deleteTareaModista(id)
    return jsonify(json)


@app.route('/tareaModista/asignar/<string:id>', methods=['PUT'])
def asignarModista(id):
    data = request.get_json()
    json = tareaModista.AsignarTareaModista(id, data)
    return jsonify(json)


@app.route('/tareaModista/responder/<string:id>', methods=['PUT'])
def responderTareaModista(id):
    data = request.get_json()
    json = tareaModista.responderTareaModista(id, data)
    return jsonify(json)


@app.route('/tareaModista/sinAsignar', methods=['GET'])
def getTareaModistaSinAsignar():
    json = tareaModista.getTareaModistaSinAsignar()
    return jsonify(json)


@app.route('/tareaModista/pendientes/<string:idModista>', methods=['GET'])
def getTareasModistaPendiente(idModista):
    json = tareaModista.getTareaModistaPendiente(idModista)
    return jsonify(json)


@app.route('/tareaModista/pendientes', methods=['GET'])
def getAllPendientesModisteria():
    json = tareaModista.getAllTareasModistaPendientes()
    return jsonify(json)


# -------TAREA LAVANDERIA-----#

@app.route('/lavanderia', methods=['POST'])
def createTareaLavanderia():
    data = request.get_json()
    response = tareaLavanderia.createLavanderia(data)
    return jsonify(response)

@app.route('/lavanderia/completed/<string:id>', methods=['GET'])
def getAllCompletedLavanderia(id):
    response = tareaLavanderia.getTaskCompleted(id)
    return jsonify(response)


@app.route('/lavanderia', methods=['GET'])
def getAllTareaLavanderia():
    response = tareaLavanderia.getAllTareaLavanderia()
    return jsonify(response)


@app.route('/lavanderia/<string:id>', methods=['GET'])
def getTareaLavanderiaById(id):
    response = tareaLavanderia.getTareaLavanderiaById(id)
    return jsonify(response)


@app.route('/lavanderia/sinAsignar', methods=['GET'])
def getAllTareaLavanderiaSinAsignar():
    response = tareaLavanderia.getSinAsignarLavanderia()
    return jsonify(response)


@app.route('/lavanderia/formulario/<string:formulario>')
def GetTareaLavanderiaByForm(formulario):
    json = tareaLavanderia.GetTareaLavanderiaByFormulario(formulario)
    return jsonify(json)


@app.route('/lavanderia/pendientes', methods=['GET'])
def getAllPendientesLavanderia():
    response = tareaLavanderia.getAllPendientes()
    return jsonify(response)


@app.route('/lavanderia/pendientes/<string:id>', methods=['GEt'])
def getpendientesByEmpleado(id):
    response = tareaLavanderia.getAllPendientesLavanderia(id)
    return jsonify(response)


@app.route('/lavanderia/<string:id>', methods=['PUT'])
def updateLavanderia(id):
    data = request.get_json()
    response = tareaLavanderia.updateTarea(id, data)
    return jsonify(response)


@app.route('/lavanderia/<string:id>', methods=['DELETE'])
def deleteLavanderia(id):
    response = tareaLavanderia.deleteTareaLavanderia(id)
    return jsonify(response)


@app.route('/lavanderia/answer/<string:id>', methods=['PUT'])
def responderLavanderia(id):
    data = request.get_json()
    response = tareaLavanderia.responderTareaLavanderia(id, data)
    return jsonify(response)


@app.route('/lavanderia/<string:id>/empleado/<string:idLavanderia>', methods=['PUT'])
def asignarLavanderia(id, idLavanderia):
    response = tareaLavanderia.asignarLavanderia(id, idLavanderia)
    return jsonify(response)


# ---------ENTREGA Y DEVOLUCION--------#
@app.route('/entregaDevolucion', methods=['POST'])
def createEntregarDevolver():
    data = request.get_json()
    response = entregaDevolver.createEntregaDevolucion(data)
    return jsonify(response)


@app.route('/entregaDevolucion', methods=['GET'])
def getAllEntregaDevolucion():
    response = entregaDevolver.getAllEntregaDevolucion()
    return jsonify(response)


@app.route('/entregaDevolucion/<string:id>', methods=['GET'])
def getEntregaDevolucioById(id):
    print("byId")
    response = entregaDevolver.getByIdEntregaDevolucion(id)
    return jsonify(response)


@app.route('/entregaDevolucion/<string:id>', methods=['PUT'])
def updateEntregaDevolucion(id):
    data = request.get_json()
    response = entregaDevolver.updateEntregaDevolucion(id, data)
    return jsonify(response)


@app.route('/entregaDevolucion/<string:id>', methods=['DELETE'])
def deleteEntregaDevolucion(id):
    response = entregaDevolver.deleteEntregaDevolucion(id)
    return jsonify(response)


@app.route('/entregaDevolucion/SinEntregar', methods=['GET'])
def getEntregaDevolucionSinEntregar():
    response = entregaDevolver.getSinEntregar()
    return jsonify(response)


@app.route('/entregaDevolucion/SinDevolver', methods=['GET'])
def getEntregaDevolucionSinDeolver():
    response = entregaDevolver.getSinDevolver()
    return jsonify(response)


@app.route('/entregaDevolucion/entrega/<string:id>', methods=['PUT'])
def responderEntrega(id):
    data = request.get_json()
    response = entregaDevolver.responderEntrega(id, data)
    return jsonify(response)


@app.route('/entregaDevolucion/devolucion/<string:id>', methods=['PUT'])
def responderDevolucion(id):
    data = request.get_json()
    response = entregaDevolver.responderDevolucion(id, data)
    return jsonify(response)


@app.route('/entregaDevolucion/formulario/<string:formulario>', methods=['GET'])
def getEntregaDevolucionByFormulario(formulario):
    json = entregaDevolver.getByFormulario(formulario)
    return jsonify(json)


@app.route('/calendar', methods=['GET'])
def calendar():
    json = calendario.tareasEnOrdenPorFecha()
    return jsonify(json)


@app.route('/calendar/<string:idAsesor>', methods=['GET'])
def calendarAsesor(idAsesor):
    json = calendario.calendarAsesor(idAsesor)
    return jsonify(json)


# ------------ CAJA ------------#
@app.route('/caja/agregar', methods=['PUT'])
def agregarCaja():
    info = request.get_json()
    json = caja.agregarSaldo(info)
    return jsonify(json)


@app.route('/caja/retirar', methods=['PUT'])
def retirarCja():
    info = request.get_json()
    json = caja.retirarSaldo(info)
    return jsonify(json)


@app.route('/caja/saldo', methods=['GET'])
def GetSaldo():
    json = caja.verSaldo()
    return jsonify(json)


@app.route('/caja/restaurar', methods=['PUT'])
def restaurarSaldoCaja():
    json = caja.restaurarSaldo()
    print(json)
    return jsonify(json)


def restaurarSaldoTarea():
    caja.restaurarSaldo()


scheduler.add_job(restaurarSaldoTarea, 'interval', days=1, start_date='2023-10-19 00:00:00')


# ----------- AUDITORIA -----------#

@app.route('/Auditoria/<string:id>', methods=['GET'])
def getRegistroById(id):
    json = audit.getRegistroById(id)
    return jsonify(json)


@app.route('/Auditoria', methods=['GET'])
def getAllResgistro():
    json = audit.getAllResgistro()
    return jsonify(json)


# -------------- Form MakeUP --------------#

@app.route('/makeup', methods=['POST'])
def CreateFormMakeup():
    data = request.get_json()
    json = makeup.create(data)
    return jsonify(json)


@app.route('/makeup', methods=['GET'])
def getAllFormMakeup():
    json = makeup.getAll()
    return jsonify(json)


@app.route('/makeup/<string:id>', methods=['GET'])
def getFormMakekupById(id):
    json = makeup.getById(id)
    return jsonify(json)


@app.route('/makeup/factura/<string:factura>', methods=['GET'])
def getFormMakeUpByFactura(factura):
    json = makeup.getByFactura(factura)
    return jsonify(json)


@app.route('/makeup/<string:id>', methods=['DELETE'])
def deleteFormMakeUpById(id):
    json = makeup.deleteMakeUpForm(id)
    return jsonify(json)


@app.route('/makeup/<string:id>', methods=['PUT'])
def updateFormMakeUp(id):
    data = request.get_json()
    json = makeup.updateMakeUpFom(id, data)
    return jsonify(json)

@app.route('/makeup/dia', methods=['GET'])
def getFormsByDia():
    infoDia = request.get_json()
    json = makeup.getTareasPorDia(infoDia)
    return json

##----------- TAREAS MAKEUP -----------##
@app.route('/tareaMakeup',methods=['POST'])
def createTareaMakeup():
    data = request.get_json()
    json = tareaMake.createTareaMakeUp(data)
    return jsonify(json)
@app.route('/tareaMakeup',methods=['GET'])
def getAllTareaMakeup():
    json = tareaMake.getAllTareaMakeUp()
    return jsonify(json)
@app.route('/tareaMakeup/<string:id>',methods=['GET'])
def getByIdTareaMakeup(id):
    json = tareaMake.getTareaMakeUpById(id)
    return jsonify(json)

@app.route('/tareaMakeup/completed/<string:id>', methods=['GET'])
def getTareaMakeupCompleted(id):
    json = tareaMake.getTaskCompleted(id)
    return jsonify(json)

@app.route('/tareaMakeup/<string:id>',methods=['PUT'])
def updateTareaMakeup(id):
    data = request.get_json()
    json = tareaMake.updateTareaMakup(id,data)
    return jsonify(json)

@app.route('/tareaMakeup/<string:id>',methods=['DELETE'])
def deleteTareaMakeup(id):
    json = tareaMake.DeleteTareaMakeup(id)
    return jsonify(json)
@app.route('/tareaMakeup/verPendientes/<string:id>',methods=['GET'])
def GetAllPendientesTareaMakeupByStylist(id):
    json = tareaMake.getAllPendientesByStylist(id)
    return jsonify(json)
@app.route('/tareaMakeup/verPendientes',methods=['GET'])
def GetAllPendientesTareaMakeup():
    json = tareaMake.getAllPendientes()
    return jsonify(json)
@app.route('/tareaMakeup/responder/<string:id>',methods=['PUT'])
def responderTareaMakeUp(id):
    data = request.get_json()
    json = tareaMake.responderTareaModista(id,data)
    return jsonify(json)

# -----------CONFIG AND MAIN ROOT-----------##
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


@app.route('/', methods=['GET'])
def test():
    consultarEIniciarTareas()
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
