import calendar

from models.FormatoAlquiler import formatoAlquiler
from models.Tarea import Tarea
from models.entregaDevolucion import entregaDevolucion
from repositories.repoEntregaDevolucion import repoEntregaDevolucion
from repositories.repositorioFormatoAlquiler import repositorioFormatoAlquiler
from repositories.repositorioTarea import repositorioTareas
from controllers.productoController import ProductoController
from controllers.cajaController import cajaController
from controllers.auditoriaController import auditoriaController

from bson import DBRef, ObjectId
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta,date

class formularioAlquilerController():
    def __init__(self):
        self.repositorioAlquiler = repositorioFormatoAlquiler()
        self.repoTareas = repositorioTareas()
        self.controllerProduct = ProductoController()
        self.repoEntrega = repoEntregaDevolucion()
        self.repoCaja = cajaController()
        self.auditoria = auditoriaController()


    def create(self, infoAlquiler):
        if self.isValid(infoAlquiler):
            db = self.repositorioAlquiler.getDb()
            job = db['jobs']
            fechaDevolucion = datetime(infoAlquiler['AñoEntrega'],infoAlquiler['MesEntrega'], infoAlquiler['DiaEntrega'],23,59,0) + timedelta(days=5)
            if fechaDevolucion.weekday() == calendar.SUNDAY:
                fechaDevolucion += timedelta(days=1)
            job.insert_one({
                "fun": "desbloquearProducto",
                "trigger": "date",
                "fecha": str(fechaDevolucion),
                "producto": infoAlquiler['idProducto'],
                "creada": False
            })
            formulario = formatoAlquiler(infoAlquiler['nombre'],infoAlquiler['apellido'],infoAlquiler['correo'],infoAlquiler['celular'],infoAlquiler['direccion'],infoAlquiler['idAsesor'] , infoAlquiler['sede'], infoAlquiler['idProducto'] , infoAlquiler['identificacion'] , infoAlquiler['AñoEntrega'] , infoAlquiler['MesEntrega'] ,
            infoAlquiler['DiaEntrega'], infoAlquiler['NumeroDeFactura'], infoAlquiler['accesorio'], infoAlquiler['velo'], infoAlquiler['aro'],
            infoAlquiler['metodoDePago'], infoAlquiler['Abono'], infoAlquiler['Saldo'], infoAlquiler['Deposito'], infoAlquiler['AñoCitaMedidas'], infoAlquiler['MesCitaMedidas'], infoAlquiler['DiaCitaMedidas'])
            dict = []
            response = self.repositorioAlquiler.save(formulario)
            self.repoCaja.agregarSaldo({"saldo": infoAlquiler['Abono'],
                                        "empleado": infoAlquiler['idAsesor'],
                                        "metodo": "Deposito",
                                        "descripcion": "Abono de parte del formulario " + response[
                                            '_id'] + "y numero de factura " + infoAlquiler['NumeroDeFactura']
                                        })
            infoTarea = self.repositorioAlquiler.getByIdToUpdate(response['_id'])
            tarea = Tarea(DBRef('formatoAlquiler',infoTarea['_id']), infoTarea['asesor'] , infoTarea['Producto'], formulario.FechaCitaDeMedidas,False,False)
            responseTarea = self.repoTareas.save(tarea,False)
            entrega = entregaDevolucion(infoAlquiler['idProducto'], infoAlquiler['idAsesor'],response['_id'],str(date(infoAlquiler['AñoEntrega'], infoAlquiler['MesEntrega'],infoAlquiler['DiaEntrega'])), False, None, False)
            responseEntrega = self.repoEntrega.save(entrega)
            dict.append(response)
            dict.append(responseTarea)
            dict.append(responseEntrega)
            return dict
        else:
            return {"status": False, "message": "el formulario no pudo ser creado, por favor revise la información suministrada"}

    def getByFactura(self,factura:str):
        print("get formulario by factura")
        return self.repositorioAlquiler.getByFactura(factura)

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

    def UpdateFormularioAlquiler(self, id, infoAlquiler):
        print("actualizar Productos")
        if(self.isValid(
            infoAlquiler
        )):
            dict = []
            form = formatoAlquiler(infoAlquiler['nombre'],infoAlquiler['apellido'],infoAlquiler['correo'],infoAlquiler['celular'],infoAlquiler['direccion'],infoAlquiler['idAsesor'] , infoAlquiler['sede'], infoAlquiler['idProducto'] , infoAlquiler['identificacion'] , infoAlquiler['AñoEntrega'] , infoAlquiler['MesEntrega'] ,
            infoAlquiler['DiaEntrega'], infoAlquiler['NumeroDeFactura'], infoAlquiler['accesorio'], infoAlquiler['velo'], infoAlquiler['aro'], infoAlquiler['total'],
            infoAlquiler['metodoDePago'], infoAlquiler['Abono'], infoAlquiler['Saldo'], infoAlquiler['Deposito'], infoAlquiler['AñoCitaMedidas'], infoAlquiler['MesCitaMedidas'], infoAlquiler['DiaCitaMedidas'])
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
        try:
            fechaEntrega = date(infoAlquiler['AñoEntrega'], infoAlquiler['MesEntrega'], infoAlquiler['DiaEntrega'])
            fechaMedidas = date(infoAlquiler['AñoCitaMedidas'], infoAlquiler['MesCitaMedidas'],infoAlquiler['DiaCitaMedidas'])
            if (True and infoAlquiler['idAsesor'] and infoAlquiler['idProducto']  and infoAlquiler['identificacion'] and infoAlquiler['sede']
                and infoAlquiler['NumeroDeFactura'] and infoAlquiler['accesorio']  and infoAlquiler['velo']
                and infoAlquiler['aro'] and infoAlquiler['metodoDePago'] and infoAlquiler['Abono'] and infoAlquiler['Saldo']
                    and infoAlquiler['Deposito'] and infoAlquiler['AñoEntrega'] and infoAlquiler['MesEntrega'] and infoAlquiler['DiaEntrega']
                    and fechaEntrega >= date.today() and fechaMedidas >= date.today()):
                return True
        except:
            return False

