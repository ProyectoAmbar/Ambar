import calendar

from models.FormatoAlquiler import formatoAlquiler
from models.Tarea import Tarea
from repositories.repositorioFormatoAlquiler import repositorioFormatoAlquiler
from repositories.repositorioTarea import repositorioTareas
from controllers.productoController import ProductoController

from bson import DBRef, ObjectId
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

class formularioAlquilerController():
    def __init__(self):
        self.repositorioAlquiler = repositorioFormatoAlquiler()
        self.repoTareas = repositorioTareas()
        self.controllerProduct = ProductoController()

    def create(self, infoAlquiler):
        if self.isValid(infoAlquiler):
            db = self.repositorioAlquiler.getDb()
            job = db['jobs']
            fechaEntrega = datetime(infoAlquiler['AñoEntrega'],infoAlquiler['MesEntrega'], infoAlquiler['DiaEntrega'],23,59,0) + timedelta(days=5)
            if fechaEntrega.weekday() == calendar.SUNDAY:
                fechaEntrega += timedelta(days=1)
            job.insert_one({
                "fun": "desbloquearProducto",
                "trigger": "date",
                "fecha": str(fechaEntrega),
                "producto": infoAlquiler['idProducto'],
                "creada": False
            })
            formulario = formatoAlquiler(infoAlquiler['idAsesor'] , infoAlquiler['idProducto'] , infoAlquiler['identificacion'] , infoAlquiler['AñoEntrega'] , infoAlquiler['MesEntrega'] ,
            infoAlquiler['DiaEntrega'], infoAlquiler['NumeroDeFactura'], infoAlquiler['accesorio'], infoAlquiler['corbatin'], infoAlquiler['velo'], infoAlquiler['aro'], infoAlquiler['total'],
            infoAlquiler['metodoDePago'], infoAlquiler['Abono'], infoAlquiler['Saldo'], infoAlquiler['Deposito'], infoAlquiler['AñoCitaMedidas'], infoAlquiler['MesCitaMedidas'], infoAlquiler['DiaCitaMedidas'])
            print(formulario)

            dict = []
            response = self.repositorioAlquiler.save(formulario)
            print(response['_id'])
            infoTarea = self.repositorioAlquiler.getByIdToUpdate(response['_id'])
            tarea = Tarea(DBRef('formulario',infoTarea['_id']), infoTarea['asesor'] , infoTarea['Producto'],infoTarea['fechaDeEntrega'],False,False)
            responseTarea = self.repoTareas.save(tarea,False)
            dict.append(response)
            dict.append(responseTarea)
            return dict
        else:
            return {"status": False, "code": 400, "message": "el formulario no pudo ser creado"}

    def getAllFormularios(self):
        print("get all Formularios Alquileres")
        return self.repositorioAlquiler.getAll()

    def getFormulariosAlquilerById(self, id):
        print("get formularios Alquiler By Id")
        response = self.repositorioAlquiler.getById(id)
        if response != None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No se encontro el formulario de Alquiler con id: " + id}

    def UpdateFormularioAlquiler(self, id, infoUpdate):
        print("actualizar Productos")
        if(self.isValid(infoUpdate)):
            dict = []
            form = formatoAlquiler(infoUpdate['idAsesor'], infoUpdate['idProducto'],infoUpdate['identificacion'], infoUpdate['AñoEntrega'],
            infoUpdate['MesEntrega'],infoUpdate['DiaEntrega'], infoUpdate['NumeroDeFactura'],infoUpdate['accesorio'], infoUpdate['corbatin'],
            infoUpdate['velo'], infoUpdate['aro'], infoUpdate['total'], infoUpdate['metodoDePago'], infoUpdate['Abono'], infoUpdate['Saldo'],
            infoUpdate['Deposito'], infoUpdate['AñoCitaMedidas'], infoUpdate['MesCitaMedidas'], infoUpdate['DiaCitaMedidas'])
            response = self.repositorioAlquiler.update(id,form)
            dict.append(response)
            dict.append({"status": True , "code": 200, "message": "El fomulario fue actualizado de manera exitosa"})
            return dict
        else:
            return {"status": False, "code": 400, "message": "Hace falta informacion para actualizar el formulario de Alquiler"}

    def Delete(self, id):
        print("actualizar productos")
        return self.repositorioAlquiler.delete(id)

    def getFormPorEntregar(self):
        print("getFormPorEntregar")
        return self.repositorioAlquiler.getEntregaDeProductos()


    def isValid(self, infoAlquiler):
        if (infoAlquiler['idAsesor'] and infoAlquiler['idProducto']  and infoAlquiler['identificacion']
            and infoAlquiler['NumeroDeFactura'] and infoAlquiler['accesorio'] != None and infoAlquiler['corbatin'] != None and infoAlquiler['velo'] != None
            and infoAlquiler['aro'] != None and infoAlquiler['total'] and infoAlquiler['metodoDePago'] and infoAlquiler['Abono'] and infoAlquiler['Saldo']
            and infoAlquiler['Deposito'] and infoAlquiler['AñoEntrega'] and infoAlquiler['MesEntrega'] and infoAlquiler['DiaEntrega']):
            return True
        else:
            return False
