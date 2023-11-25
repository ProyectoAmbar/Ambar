from models.tareaMakeup import tareaMakeup
from repositories.repoTareaMakeUp import repoTareaMakeup

class tareaMakeupController:
    def __init__(self):
        self.repoTareaMakeup = repoTareaMakeup()

    def isValid(self,infoTareaMakeUp):
        try:
            if (infoTareaMakeUp['maquilladora'] != None and infoTareaMakeUp['referencia'] != None and infoTareaMakeUp['formulario'] != None
                and infoTareaMakeUp['tipoMakeUp'] != None and infoTareaMakeUp['completado'] != None and infoTareaMakeUp['fecha'] != None):
                return True
        except:
            return False

    def createTareaMakeUp(self,infoTareaMakeUp):
        if (self.isValid(infoTareaMakeUp)):
            tarea = tareaMakeup(infoTareaMakeUp['maquilladora'], infoTareaMakeUp['formulario'],
                                infoTareaMakeUp['referencia'], infoTareaMakeUp['tipoMakeUp'], infoTareaMakeUp['fecha'],
                                infoTareaMakeUp['completado'])
            return self.repoTareaMakeup.save(tarea)
        else:
            return {"status": False, "code": 400, "message": "La información para crear la tarea no es correcta"}

    def getTareaMakeUpById(self, id):
        return self.repoTareaMakeup.getById(id)

    def getAllTareaMakeUp(self):
        return self.repoTareaMakeup.getAll()

    def updateTareaMakup(self, id, infoTareaMakeUp):
        search = self.repoTareaMakeup.getById(id)
        if self.isValid(infoTareaMakeUp) and search is not None:
            tarea = tareaMakeup(infoTareaMakeUp['maquilladora'], infoTareaMakeUp['formulario'],
                                infoTareaMakeUp['referencia'], infoTareaMakeUp['tipoMakeUp'], infoTareaMakeUp['fecha'],
                                infoTareaMakeUp['completado'])

    def DeleteTareaMakeup(self,id):
        return self.repoTareaMakeup.delete(id)

    def getAllPendientesByStylist(self,idMakeup):
        return self.repoTareaMakeup.getAllPendientesByStylist(idMakeup)

    def getAllPendientes(self):
        return self.repoTareaMakeup.getAllPendientes()

    def getAllSinAsignar(self):
        return self.repoTareaMakeup.getAllMakeupSinAsignar()

    def responderTareaModista(self,id,infoTareaMakeUp):
        search = self.repoTareaMakeup.getByIdToUpdate(id)
        if search['completado'] is True:
            return {"message": "la tarea ya ha finalizado"}
        elif search is not None and infoTareaMakeUp['completado'] != None:
            tarea = tareaMakeup(search['maquilladora'], search['formulario'],
                                search['referencia'], search['tipoMakeUp'], search['fecha'],
                                infoTareaMakeUp['completado'])
            response = self.repoModista.update(id, tarea)

            return response

        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrado la tarea de Modisteria con id" + id}

