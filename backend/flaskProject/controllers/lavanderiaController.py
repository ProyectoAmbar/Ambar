from models.tareaLavanderia import tareaLavanderia
from repositories.repositorioLavanderia import repoLavanderia
class lavanderiaController():
    def __init__(self):
        self.repoLavanderia = repoLavanderia()

    def isValid( self, infoLavanderia):
        try:
            if infoLavanderia['lavanderia'] != None and infoLavanderia['producto'] != None and infoLavanderia['fecha'] != None and infoLavanderia['completado'] != None:
                return True
        except:
            return False
    def createLavanderia(self, infoLavanderia):
        if self.isValid(infoLavanderia):
            lavanderia = tareaLavanderia(infoLavanderia['lavanderia'] , infoLavanderia['producto'] , infoLavanderia['fecha'] , infoLavanderia['completado'])
            return self.repoLavanderia.save(lavanderia)
        else:
            return {"status":False, "code": 400, "message": "No tiene la información apropidada para crear una tarea de lavanderia"}

    def getAllTareaLavanderia(self):
        return self.repoLavanderia.getAll()

    def getTareaLavanderiaById(self, id):
        response = self.repoLavanderia.getById(id)
        if response is not None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No fue posible encontrar la tarea con id:" + id}

    def updateTarea(self, id, infoUpdate):
        search = self.repoLavanderia.getById(id)
        if search is not None and self.isValid(infoUpdate):
            tarea = tareaLavanderia(infoUpdate['lavanderia'], infoUpdate['producto'], infoUpdate['fecha'], infoUpdate['completado'])
            return self.repoLavanderia.update(id, tarea)
        else:
            return {"status": False, "code": 400, "message": "no fue posible encontrar la tarea, o la información a actualizar es erronea"}

    def deleteTareaLavanderia(self,id):
        return self.repoLavanderia.delete(id)

    def responderTareaLavanderia(self, id, infoUpdate):
        search = self.repoLavanderia.getByIdToUpdate(id)
        if search['completado'] is False:
            tarea = tareaLavanderia(search['lavanderia'], search['producto'], search['fecha'], infoUpdate['completado'])
            return self.repoLavanderia.update(id, tarea)
        else:
            return {"status": False, "code": 400, "message": "la tarea ya fue completada"}

    def asignarLavanderia(self, id, idLavanderia):
        search = self.repoLavanderia.getByIdToUpdate(id)
        if search is not None:
            tarea = tareaLavanderia(idLavanderia,search['producto'], search['fecha'], False)
            return self.repoLavanderia.update(id, tarea)
        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrada la tarea"}

