from repositories.repositorioTareaModista import repoTareaModista
from repositories.repositorioFormMedidas import repositorioFormMedidas
from models.tareaModisteria import tareaModisteria
from bson import DBRef, ObjectId
import re

class tareaModisteriaController():
    def __init__(self):
        self.repoModista = repoTareaModista()
        self.repoFormMedidas = repositorioFormMedidas()

    def Create(self, infoTareaModisteria):
        print("crear Tarea Modisteria")
        if self.isValid(infoTareaModisteria):
            tareaModista = tareaModisteria(infoTareaModisteria['formMedidas'], infoTareaModisteria['modista'],infoTareaModisteria['producto'],
                            infoTareaModisteria['preciosCompletado'], infoTareaModisteria['completado'])
            return self.repoModista.save(tareaModista)

        else:
            return {"status": False, "code": 400, "message": "no se tiene la información necesaria para crear la tarea de Modisteria"}

    def getAllTareaModista(self):
        print("get all tarea Modista")
        return self.repoModista.getAll()

    def getTareaModistaById(self,id):
        print("get tarea modista by id")
        return self.repoModista.getById(id)

    def updateTareaModista(self,id,infoTareaModisteria):
        search = self.repoModista.getById(id)
        if self.isValid(infoTareaModisteria) and search is not None:
            tareaModista = tareaModisteria(infoTareaModisteria['formMedidas'],infoTareaModisteria['modista'],infoTareaModisteria['producto'],
                            infoTareaModisteria['preciosCompletado'], infoTareaModisteria['completado'])
            return self.repoModista.update(id, tareaModista)
        elif search is None:
            return {"status": False, "code": 400, "message": "No ha sido encontrado la tarea de Modisteria con id" + id}
        else:
            return {"status": False, "code": 400, "message": "no se tiene la información necesaria para crear la tarea de Modisteria"}

    def deleteTareaModista(self,id):
        search = self.repoModista.getById(id)
        if search is not None:
            return self.repoModista.delete(id)
        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrado la tarea de Modisteria con id" + id}

    def getTareaModistaSinAsignar(self):
        return self.repoModista.getTareasSinAsignar()

    def getTareaModistaPendiente(self,idEmpleado):
        return self.repoModista.getTareasPendientes(idEmpleado)
    def AsignarTareaModista(self,id, infoTareaModisteria):
        search = self.repoModista.getByIdToUpdate(id)
        if search is not None:
            tareaModista = tareaModisteria(search['formMedidas'],search['modista'],search['producto'],
                            search['preciosCompletado'], search['completado'])
            return self.repoModista.update(id,tareaModista)
        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrado la tarea de Modisteria con id" + id}

    def responderTareaModista(self,id,infoTareaModisteria):
        search = self.repoModista.getByIdToUpdate(id)
        if search is not None and infoTareaModisteria['completado']!= None:
            print(str(search['formMedidas'].id))
            comprobarPrecios = self.repoFormMedidas.getById(str(search['formMedidas'].id))
            preciosCompletado = all(arr["precio"] is not None for arr in comprobarPrecios['arreglos'])
            if preciosCompletado is True:
                tareaModista = tareaModisteria(search['formMedidas'],search['modista'],
                            search['producto'],True, infoTareaModisteria['completado'])
                return self.repoModista.update(id, tareaModista)
            else:
                return {"status": False, "message": "no se han colocado los precios al formato de medidas"}
        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrado la tarea de Modisteria con id" + id}


    def isValid(self,infoTareaModisteria):
        if (infoTareaModisteria['modista'] != None and infoTareaModisteria['producto'] != None
                and infoTareaModisteria['preciosCompletado'] != None and infoTareaModisteria['completado'] != None):
            return True
        else:
            return False


