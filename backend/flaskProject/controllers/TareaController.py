from repositories.repositorioTarea import repositorioTareas
from models.Tarea import Tarea

class tareaController():
    def __init__(self):
        self.repositorioTareas = repositorioTareas()
    def Create(self, infoTarea):
       # try:
            if infoTarea['idAsesor']!= None  and infoTarea['idProducto']!= None and infoTarea['estado'] != None :
                tarea = Tarea(infoTarea['idAsesor'] , infoTarea['idEmpleado'] , infoTarea['idProducto'] , infoTarea['mensaje'] , infoTarea['estado'] , infoTarea['observaciones'])
                return self.repositorioTareas.save(tarea, infoTarea['estado'])
            else:
                return {"status": False, "code": 400, "message": "no se tiene la información necesaria para crear la tarea"}
       # except KeyError:
              #  tarea = Tarea(infoTarea['idAsesor'], infoTarea['idProducto'], infoTarea['estado'])
               # return self.repositorioTareas.save(tarea, infoTarea['estado'])

         #   return {"status": False, "code": 400, "message": "no se pudo crear la tarea"}


