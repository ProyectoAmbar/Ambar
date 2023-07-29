from repositories.repoEntregaDevolucion import repoEntregaDevolucion
from models.entregaDevolucion import entregaDevolucion

class entregaDevolucionController():
    def __init__(self):
        self.repoEntrega = repoEntregaDevolucion()

    def createEntregaDevolucion(self,infoEntrega):
        try:
            entrega = entregaDevolucion(infoEntrega['asesor'],infoEntrega['producto'],infoEntrega['fechaEntrega'],infoEntrega['entregaCompletado'], infoEntrega['fechaDevolucion'],infoEntrega['devolucionCompletado'])
            response = self.repoEntrega.save(entrega)
            return response
        except:
            return {"status": False, "code": 400, "message": "no fue posible crear la tarea de entrega y devolucion"}

    def getAllEntregaDevolucion(self):
        return self.repoEntrega.getAll()

    def getByIdEntregaDevolucion(self,id):
        response = self.repoEntrega.getById(id)
        if response is not None:
            return response
        else:
            return {"status": False, "code": 400, "message": "no fue posible crear la tarea de entrega y devolucion"}

    def updateEntregaDevolucion(self, id, infoUpdate):
        try:
            entrega = entregaDevolucion(infoUpdate['asesor'], infoUpdate['producto'], infoUpdate['fechaEntrega'],infoUpdate['entregaCompletado'], infoUpdate['fechaDevolucion'],infoUpdate['devolucionCompletado'])
            response = self.repoEntrega.update(id,entrega)
            return response
        except:
            return {"status": False, "code": 400, "message": "no fue posible crear la tarea de entrega y devolucion"}

    def deleteEntregaDevolucion(self,id):
        return self.repoEntrega.delete(id)

    def getSinEntregar(self):
        return self.repoEntrega.getAllSinEntregar()

    def getSinDevolver(self):
        return self.repoEntrega.getAllSinDevolver()

    def responderEntrega(self,id,infoUpdate):
        search = self.repoEntrega.getByIdToUpdate(id)
        if infoUpdate['entregaCompletado'] is True:
            entrega = entregaDevolucion(search['producto'], search['asesor'], search['fechaEntrega'],infoUpdate['entregaCompletado'],infoUpdate['fechaDevolucion'],infoUpdate['devolucionCompletado'])
            return self.repoEntrega.update(id, entrega)
        else:
            return {"message": "No se ha completado la tarea"}

    def responderDevolucion(self, id, infoUpdate):
        search = self.repoEntrega.getByIdToUpdate(id)
        entrega = entregaDevolucion(search['producto'], search['asesor'], search['fechaEntrega'],search['entregaCompletado'],search['fechaDevolucion'],infoUpdate['devolucionCompletado'])
        return self.repoEntrega.update(id, entrega)



