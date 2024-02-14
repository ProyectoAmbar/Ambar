from models.formatoFotos import formatoFotos
from repositories.repoFotos import RepoFotos
from datetime import datetime

class fotosController():
    def __init__(self):
        self.repoFotos = RepoFotos()

    def isValid(self, infoFotos):
        try:
            if (infoFotos['dia'] and infoFotos['mes'] and infoFotos['año'] and infoFotos['hora'] and infoFotos['minutos']
                    and infoFotos['fv'] and infoFotos['locacion'] and infoFotos['referencia'] and infoFotos[
                        'nombreCliente'] and infoFotos['numeroCliente'] and infoFotos['correoCliente']):
                return True
        except:
            return False

    def getSinCompletar(self):
        self.repoFotos.getSinCompletar()

    def create(self, infoFotos):
        if (self.isValid(infoFotos)):
            fecha = datetime(infoFotos['año'], infoFotos['mes'], infoFotos['dia'], infoFotos['hora'],infoFotos['minutos'],0)
            formFotos = formatoFotos(fecha, infoFotos['fv'], infoFotos['locacion'],infoFotos['referencia'], infoFotos['nombreCliente'], infoFotos['numeroCliente'],infoFotos['correoCliente'], False)
            return self.repoFotos.save(formFotos)
        else:
            return {"status": False, "code": 400,
                    "message": "Por favor ingrese la información necesaria para crear la tarea de fotos"}

    def update(self, id, infoFotos):
        if (self.isValid(infoFotos)):
            fecha = datetime(infoFotos['año'], infoFotos['mes'], infoFotos['dia'], infoFotos['hora'],infoFotos['minutos'], 0)
            formFotos = formatoFotos(fecha , infoFotos['fv'], infoFotos['locacion'],infoFotos['referencia'], infoFotos['nombreCliente'], infoFotos['numeroCliente'],infoFotos['correoCliente'], infoFotos['estado'])
            return self.repoFotos.update(id, formFotos)
        else:
            return {"status": False, "code": 400,
                    "message": "Por favor ingrese la información necesaria para crear la tarea de fotos"}

    def getAll(self):
        return self.repoFotos.getAll()

    def getById(self, id):
        return self.repoFotos.getById(id)

    def delete(self, id):
        return self.repoFotos.delete(id)

    def responderTarea(self, id, infoFotos):
        search = self.repoFotos.getById(id)
        if search['estado'] is False:
            formFotos = formatoFotos(search['fecha'], search['fv'], search['locacion'], search['referencia'],
                                     search['nombreCliente'], search['numeroCliente'], search['correoCliente'], infoFotos['estado'])
            return self.repoFotos.update(id, formFotos)
        else:
            return {"message": "la tarea ha finalizado"}
