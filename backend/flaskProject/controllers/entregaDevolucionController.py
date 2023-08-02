from repositories.repoEntregaDevolucion import repoEntregaDevolucion
from controllers.productoController import ProductoController
from models.entregaDevolucion import entregaDevolucion



from datetime import datetime


def validar_fecha_devolucion(fechaInicio_str, fechaDevolucion_str):
    try:
        fechaInicio = datetime.strptime(fechaInicio_str, "%Y-%m-%d")
        fechaDevolucion = datetime.strptime(fechaDevolucion_str, "%Y-%m-%d")
        diferencia_dias = (fechaDevolucion - fechaInicio).days
        if diferencia_dias > 8:
            return False
        else:
            return True
    except ValueError:

        return False



class entregaDevolucionController():
    def __init__(self):
        self.repoEntrega = repoEntregaDevolucion()
        self.productoControler = ProductoController()

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
            return {"status": False, "code": 400, "message": "no fue posible encontrar la tarea de entrega y devolucion con id: " + id}

    def updateEntregaDevolucion(self, id, infoUpdate):
        try:
            entrega = entregaDevolucion(infoUpdate['asesor'], infoUpdate['producto'], infoUpdate['fechaEntrega'],infoUpdate['entregaCompletado'], infoUpdate['fechaDevolucion'],infoUpdate['devolucionCompletado'])
            response = self.repoEntrega.update(id,entrega)
            return response
        except:
            return {"status": False, "code": 400, "message": "no fue posible actualizar la tarea de entrega y devolucion"}

    def deleteEntregaDevolucion(self,id):
        return self.repoEntrega.delete(id)

    def getSinEntregar(self):
        return self.repoEntrega.getAllSinEntregar()

    def getSinDevolver(self):
        return self.repoEntrega.getAllSinDevolver()

    def getSinEntregarByAsesor(self,id):
        return self.repoEntrega.getAllSinEntregarByAsesor(id)

    def getSinDevolverByAsesor(self,id):
        return self.repoEntrega.getAllSinDevolverByAsesor(id)

    def responderEntrega(self,id,infoUpdate):
        try:
            search = self.repoEntrega.getByIdToUpdate(id)
            if search['entregaCompletado'] is True:
                return {"message": "la entrega ya se a realizado"}
            elif infoUpdate['entregaCompletado'] is True:
                if validar_fecha_devolucion(search['fechaEntrega'], infoUpdate['fechaDevolucion']):
                    entrega = entregaDevolucion(search['producto'], search['asesor'], search['fechaEntrega'],
                                                infoUpdate['entregaCompletado'], infoUpdate['fechaDevolucion'], False)
                    return self.repoEntrega.update(id, entrega)
                else:
                    return {"status":False, "code": 400, "message": "la fecha de devolucion es mayor a 8 días"}
            else:
                return {"message": "No se ha completado la tarea"}
        except:
            return {"status": False, "code": 400, "message": "Hace falta infomación"}

    def responderDevolucion(self, id, infoUpdate):
        search = self.repoEntrega.getByIdToUpdate(id)
        if search['devolucionCompletado'] is True:
            return {"message": "la tarea ya se ha completado"}
        else:
            entrega = entregaDevolucion(search['producto'], search['asesor'], search['fechaEntrega'],search['entregaCompletado'],search['fechaDevolucion'],infoUpdate['devolucionCompletado'])
            producto = self.productoControler.desbloquearProducto(str(search['producto'].id))
            return self.repoEntrega.update(id, entrega)



