from repositories.repositorioTarea import repositorioTareas
from models.Tarea import Tarea

class tareaController():
    def __init__(self):
        self.repositorioTareas = repositorioTareas()
    def Create(self, infoTarea):
        print("crear tarea")
        if infoTarea['idAsesor']!= None  and infoTarea['idProducto']!= None and infoTarea['estado'] != None :
            tarea = Tarea(infoTarea['idAsesor'] , infoTarea['idEmpleado'] , infoTarea['idProducto'] , infoTarea['mensaje'] , infoTarea['estado'] , infoTarea['observaciones'])
            return self.repositorioTareas.save(tarea, infoTarea['estado'])
        else:
            return {"status": False, "code": 400, "message": "no se tiene la información necesaria para crear la tarea"}

    def getAllTareas(self):
        print("get all tareas")
        return self.repositorioTareas.getAll()

    def getById(self,_id):
        print("get producto by id")
        response =  self.repositorioTareas.getById(_id)
        if response != None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No se encontro la tarea con id: " + _id}

    def Update(self, id, infoUpdate):
        print("actualizar Tarea")
        if infoUpdate['idAsesor'] != None and infoUpdate['idProducto'] != None and infoUpdate['estado'] != None:
            response = self.repositorioTareas.update(id, Tarea(infoUpdate['idAsesor'], infoUpdate['idEmpleado'], infoUpdate['idProducto'], infoUpdate['mensaje'], infoUpdate['estado'], infoUpdate['observaciones']))
            response.append({"status": True, "code": 200, "message": "La tarea fue actualizada"})
            return response
        else:
            return {"status": False, "code": 400, "message": "Hace falta informacion para actualizar el producto"}

    def responderTarea(self, id, infoUpdate):
        search = self.repositorioTareas.getById(id)
        if (search is not None and (infoUpdate['estado'] != None and infoUpdate['observaciones'])):
            search['estado'] = infoUpdate['estado']
            search['observaciones'] = infoUpdate['observaciones']
            TAREA = Tarea(search['asesor'], search['empleado'], search['producto'], search['mensaje'], search['estado'], search['observaciones'])
            response = self.repositorioTareas.update(id,TAREA)
            return response
        elif infoUpdate['observaciones'] is None and infoUpdate['estado']!= None:
            search['observaciones'] = ""
            TAREA = Tarea(search['asesor'], search['empleado'], search['producto'], search['mensaje'], search['estado'],search['observaciones'])
            response = self.repositorioTareas.update(id,TAREA)
            return response
        else:
            return {"status": False, "code": 400, "message": "Hace falta informacion para responder la tarea"}


    def asignarTarea(self, id, infoTarea):
        search = self.repositorioTareas.getById(id)
        if search != None and infoTarea['empleado'] != None and infoTarea['mensaje'] != None:
            search['empleado'] = infoTarea['empleado']
            search['mensaje'] = infoTarea['mensaje']
            TAREA = Tarea(search['asesor'], search['empleado'], search['producto'], search['mensaje'], search['estado'],search['observaciones'])
            response = self.repositorioTareas.update(id, TAREA)
            return response
        else:
            return {"status": False, "code": 400, "message": "Hace falta infomracion para asignar la tarea"}

    def verTareasPendientes(self, id):
        search = self.repositorioTareas.getTareasPendientes(id)
        return search








    def Delete(self, id):
        print("eliminar un producto")
        return self.repositorioTareas.delete(id)





