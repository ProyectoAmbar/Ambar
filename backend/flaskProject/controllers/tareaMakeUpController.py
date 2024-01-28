from models.tareaMakeup import tareaMakeup
from repositories.repoTareaMakeUp import repoTareaMakeup
from datetime import datetime
class tareaMakeupController:
    def __init__(self):
        self.repoTareaMakeup = repoTareaMakeup()

    def isValid(self,infoTareaMakeUp):
        try:
            if (infoTareaMakeUp['maquilladora'] != None and infoTareaMakeUp['referencia'] != None and infoTareaMakeUp['formulario'] != None
                and infoTareaMakeUp['tipoMakeUp'] != None and infoTareaMakeUp['completado'] != None and infoTareaMakeUp['AñoMakeup'] != None
                and infoTareaMakeUp['MesMakeup'] != None and infoTareaMakeUp['DiaMakeup'] != None and infoTareaMakeUp['HoraMakeup'] != None
            and infoTareaMakeUp['MinutosMakeup'] != None):
                return True
        except:
            return False

    def createTareaMakeUp(self,infoTareaMakeUp):
        fecha = None
        try:
            fecha = datetime(infoTareaMakeUp['AñoMakeup'], infoTareaMakeUp['MesMakeup'], infoTareaMakeUp['DiaMakeup'],
                             infoTareaMakeUp['HoraMakeup'], infoTareaMakeUp['MinutosMakeup'], 00)
        except:
            return {"error en la fecha ingresada"}
        print(fecha)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if self.isValid(infoTareaMakeUp) and str(fecha) > str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
            search = self.repoTareaMakeup
            tarea = tareaMakeup(infoTareaMakeUp['maquilladora'], infoTareaMakeUp['formulario'],
                                infoTareaMakeUp['referencia'], infoTareaMakeUp['tipoMakeUp'], fecha,
                                infoTareaMakeUp['completado'])

            return self.repoTareaMakeup.save(tarea)
        else:
            return {"status": False, "code": 400, "message": "La información para crear la tarea no es correcta"}

    def getTareaMakeUpById(self, id):
        return self.repoTareaMakeup.getById(id)

    def getTaskCompleted(self,id):
        return self.repoTareaMakeup.getCompletedTask(id)

    def getAllTareaMakeUp(self):
        return self.repoTareaMakeup.getAll()
    def getByFactura(self,factura):
        return self.repoTareaMakeup.getByFactura()

    def updateTareaMakup(self, id, infoTareaMakeUp):
        fecha = None
        try:
            fecha = datetime(infoTareaMakeUp['AñoMakeup'], infoTareaMakeUp['MesMakeup'], infoTareaMakeUp['DiaMakeup'],
                             infoTareaMakeUp['HoraMakeup'], infoTareaMakeUp['MinutosMakeup'], 00)
        except:
            return {"error en la fecha ingresada"}
        search = self.repoTareaMakeup.getById(id)
        if self.isValid(infoTareaMakeUp) and search is not None:
            tarea = tareaMakeup(infoTareaMakeUp['maquilladora'], infoTareaMakeUp['formulario'],
                                infoTareaMakeUp['referencia'], infoTareaMakeUp['tipoMakeUp'], fecha,
                                infoTareaMakeUp['completado'])
            return self.repoTareaMakeup.update(id,tarea)
        else:
            return {"status": False, "code": 400, "message": "la información no se valida, o no se encontro el id"}

    def DeleteTareaMakeup(self,id):
        return self.repoTareaMakeup.delete(id)

    def getAllPendientesByStylist(self,idMakeup):
        return self.repoTareaMakeup.getAllPendientesByStylist(idMakeup)

    def getAllPendientes(self):
        return self.repoTareaMakeup.getAllPendientes()


    def responderTareaModista(self,id,infoTareaMakeUp):
        search = self.repoTareaMakeup.getByIdToUpdate(id)
        if search['completado'] is True:
            return {"message": "la tarea ya ha finalizado"}
        elif search is not None and infoTareaMakeUp['completado'] != None:
            tarea = tareaMakeup(search['idMakeup'], search['formulario'],
                                search['referencia'], search['tipoMakeup'], search['fecha'],
                                infoTareaMakeUp['completado'])
            response = self.repoTareaMakeup.update(id, tarea)

            return response

        else:
            return {"status": False, "code": 400, "message": "No ha sido encontrado la tarea de Modisteria con id" + id}

