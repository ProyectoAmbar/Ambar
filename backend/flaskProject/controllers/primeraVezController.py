from models.citaPrimeraVez import citaPrimeraVez
from repositories.primeraVezRepository import primeraVezRepository
from datetime import datetime


def isValid(infoCita):
    try:
        if (infoCita['nombre'] and infoCita['apellido']  and infoCita['direccion'] and infoCita[
            'telefono'] and infoCita['motivo'] and infoCita['dia'] and infoCita['mes'] and
                infoCita['año'] and infoCita['hora'] and infoCita['minuto']):
            return True
    except:
        return False


class primeraVezController():
    def __init__(self):
        self.repoPrimeraVez = primeraVezRepository()


    def createCitaPrimeraVez(self, infoCita):
        if (isValid(infoCita)):
            fecha = datetime(infoCita['año'], infoCita['mes'], infoCita['dia'], infoCita['hora'], infoCita['minuto'], 0)
            cita = citaPrimeraVez(infoCita['nombre'], infoCita['apellido'], infoCita['asesor'], infoCita['direccion'],
                                  infoCita['telefono'], infoCita['motivo'], infoCita['estado'], fecha)
            return self.repoPrimeraVez.save(cita)
        else:
            return {"status": False, "code": 400, "message": "No fue posible crear la cita de primera vez"}

    def getAllCitas(self):
        return self.repoPrimeraVez.getAll()

    def getCitasById(self, id):
        return self.repoPrimeraVez.getById(id)

    def updateCita(self, id, infoCita):
        search = self.repoPrimeraVez.getByIdToUpdate(id)
        if (isValid(infoCita)) and search['_id']:
            fecha = datetime(infoCita['año'], infoCita['mes'], infoCita['dia'], infoCita['hora'], infoCita['minuto'], 0)
            cita = citaPrimeraVez(infoCita['nombre'], infoCita['apellido'], infoCita['asesor'], infoCita['direccion'],
                                  infoCita['telefono'], infoCita['motivo'], infoCita['estado'], fecha)
            return self.repoPrimeraVez.update(id, cita)
        else:
            return {"status": False, "code": 400, "message": "No fue posible actualizar la cita de primera vez"}

    def getSinAsignar(self):
        return self.repoPrimeraVez.getCitasSinAsignar()

    def getSinCompletar(self):
        return self.repoPrimeraVez.getCitasSinCompletar()

    def getSinCompletarByAsesor(self, id):
        return self.repoPrimeraVez.getCitaSinCompletarByAsesor(id)

    def responder(self, id, respuestaCita):
        infoCita = self.repoPrimeraVez.getByIdToUpdate(id)
        if infoCita['estado'] is True:
            return {"message": "La Cita ya ha sido completada"}
        else:
            cita = citaPrimeraVez(infoCita['nombre'], infoCita['apellido'], infoCita['asesor'], infoCita['direccion'],
                                  infoCita['telefono'], infoCita['motivo'], respuestaCita['estado'], infoCita['fecha'])
            return self.repoPrimeraVez.update(id, cita)

    def deleteCita(self, id):
        search = self.repoPrimeraVez.getById(id)
        try:
            if search['_id']:
                return self.repoPrimeraVez.delete(id)
        except:
            return {"message": "No fue posible encontrar la cita con id: " + id}

    def asignarAsesor(self,id,asesor):
        infoCita = self.repoPrimeraVez.getByIdToUpdate(id)
        try:
            if infoCita['_id']:
                cita = citaPrimeraVez(infoCita['nombre'], infoCita['apellido'], asesor, infoCita['direccion'],
                                  infoCita['telefono'], infoCita['motivo'], infoCita['estado'], infoCita['fecha'])
                return self.repoPrimeraVez.update(id,cita)
        except:
            return {"message": "No se encontro la cita"}


