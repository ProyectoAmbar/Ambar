from repositories.repositorioTarea import repositorioTareas
from models.Tarea import Tarea


class tareaController():
    def __init__(self):
        self.repositorioTareas = repositorioTareas()

    def Create(self, infoTarea):
        print("crear tarea")
        if (infoTarea['formulario'] != None and infoTarea['producto'] != None and infoTarea['asesor']!=None and
            infoTarea['estado'] != None and infoTarea['fechaCitaDeMedidas'] != None and infoTarea['necesitaModista']!=None):
            tarea = Tarea(infoTarea['formulario'], infoTarea['producto'], infoTarea['asesor'],
                          infoTarea['estado'], infoTarea['fechaCitaDeMedidas'], infoTarea['necesitaModista'])
            return self.repositorioTareas.save(tarea, infoTarea['estado'])
        else:
            return {"status": False, "code": 400, "message": "no se tiene la información necesaria para crear la tarea"}

    def getAllTareas(self):
        print("get all tareas")
        return self.repositorioTareas.getAll()

    def getById(self, _id):
        print("get producto by id")
        response = self.repositorioTareas.getById(_id)
        if response != None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No se encontro la tarea con id: " + _id}

    def Update(self, id, infoUpdate):
        print("actualizar Tarea")
        if (infoUpdate['formulario'] != None and infoUpdate['producto'] != None and infoUpdate['asesor'] != None and
            infoUpdate['estado'] != None and infoUpdate['fechaCitaDeMedidas'] != None and infoUpdate['necesitaModista'] != None):

            response = self.repositorioTareas.update(id, Tarea(infoUpdate['formulario'], infoUpdate['producto'], infoUpdate['asesor'],
                          infoUpdate['estado'], infoUpdate['fechaCitaDeMedidas'], infoUpdate['necesitaModista']))

            response.append({"status": True, "code": 200, "message": "La tarea fue actualizada"})
            return response
        else:
            return {"status": False, "code": 400, "message": "Hace falta informacion para actualizar el producto"}

    def responderTareaC(self, id, infoUpdate):
        search = self.repositorioTareas.getById(id)
        if (search is not None and (infoUpdate['estado'] != None and infoUpdate['necesitaModista'])):
            search['estado'] = infoUpdate['estado']
            search['observaciones'] = infoUpdate['observaciones']
            TAREA = Tarea(search['asesor'], search['producto'], search['mensaje'], search['estado'],
                          search['observaciones'])
            response = self.repositorioTareas.update(id, TAREA)
            return response
        elif infoUpdate['observaciones'] is None and infoUpdate['estado'] != None:
            search['observaciones'] = ""
            TAREA = Tarea(search['asesor'], search['producto'], search['mensaje'], search['estado'],
                          search['observaciones'])
            response = self.repositorioTareas.update(id, TAREA)
            return response
        else:
            return {"status": False, "code": 400, "message": "Hace falta informacion para responder la tarea"}

    def verTareasPendientes(self, id):
        search = self.repositorioTareas.getTareasPendientes(id)
        return search

    def Delete(self, id):
        print("eliminar un producto")
        return self.repositorioTareas.delete(id)
