from models.tareaLavanderia import tareaLavanderia
from repositories.repositorioLavanderia import repoLavanderia
from controllers.productoController import ProductoController
import re


def validar_formato_fecha(fecha_str):
    patron = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(patron, fecha_str):
        return True
    else:
        return False

class lavanderiaController():
    def __init__(self):
        self.repoLavanderia = repoLavanderia()
        self.productoController = ProductoController()



    def isValid( self, infoLavanderia):
        try:
            if infoLavanderia['producto'] != None and infoLavanderia['formulario'] != None and infoLavanderia['fecha'] != None and validar_formato_fecha(infoLavanderia['fecha']) is True and infoLavanderia['completado'] != None:
                return True
            elif validar_formato_fecha(infoLavanderia['fecha']) is False:
                return False
        except:
            return False
    def createLavanderia(self, infoLavanderia):
        if self.isValid(infoLavanderia):
            lavanderia = tareaLavanderia(infoLavanderia['lavanderia'] , infoLavanderia['producto'] , infoLavanderia['formulario'], infoLavanderia['fecha'] , infoLavanderia['completado'], infoLavanderia['postEntrega'])
            return self.repoLavanderia.save(lavanderia)
        else:
            return {"status":False, "code": 400, "message": "No tiene la información apropidada para crear una tarea de lavanderia"}

    def getAllTareaLavanderia(self):
        return self.repoLavanderia.getAll()

    def getTaskCompleted(self, id):
        return self.repoLavanderia.getCompletedTask(id)

    def GetTareaLavanderiaByFormulario(self,formulario):
        return self.repoLavanderia.GetByFormulario(formulario)

    def getTareaLavanderiaById(self, id):
        response = self.repoLavanderia.getById(id)
        if response is not None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No fue posible encontrar la tarea con id:" + id}

    def updateTarea(self, id, infoUpdate):
        search = self.repoLavanderia.getById(id)
        if search is not None and self.isValid(infoUpdate):
            tarea = tareaLavanderia(infoUpdate['lavanderia'], infoUpdate['producto'], infoUpdate['formulario'],infoUpdate['fecha'], infoUpdate['completado'], infoUpdate['postEntrega'])
            return self.repoLavanderia.update(id, tarea)
        else:
            return {"status": False, "code": 400, "message": "no fue posible encontrar la tarea, o la información a actualizar es erronea"}

    def deleteTareaLavanderia(self,id):
        return self.repoLavanderia.delete(id)

    def responderTareaLavanderia(self, id, infoUpdate):
        search = self.repoLavanderia.getByIdToUpdate(id)
        if search['completado'] is False:
            if search['postEntrega'] is False:
                tarea = tareaLavanderia(search['lavanderia'], search['producto'], search['formulario'],search['fecha'], infoUpdate['completado'], search['postEntrega'])
                return self.repoLavanderia.update(id, tarea)
            else:
                tarea = tareaLavanderia(search['lavanderia'], search['producto'], search['formulario'], search['fecha'],
                                        infoUpdate['completado'], search['postEntrega'])
                self.productoController.desbloquearProducto(str(search['producto'].id))
                return self.repoLavanderia.update(id, tarea)
        else:
            return {"status": False, "code": 400, "message": "la tarea ya fue completada"}

    def asignarLavanderia(self, id, idLavanderia):
        search = self.repoLavanderia.getByIdToUpdate(id)
        if search is not None:
            tarea = tareaLavanderia(idLavanderia,search['producto'],search['formulario'], search['fecha'], False, search['postEntrega'])
            return self.repoLavanderia.update(id, tarea)
        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrada la tarea"}

    def getSinAsignarLavanderia(self):
        return self.repoLavanderia.getTareasSinAsignar()

    def getAllPendientes(self):
        return self.repoLavanderia.getTareasAllPendientes()

    def getAllPendientesLavanderia(self,idLavanderia):
        return self.repoLavanderia.getAlltareasPendientesLavanderia(idLavanderia)