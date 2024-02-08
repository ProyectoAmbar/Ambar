from bson import DBRef, ObjectId
from datetime import datetime

class citaPrimeraVez:
    def __init__(self,idAsesor, nombre,apellido,direccion,telefono,motivo,estado:bool, fecha):
        if isinstance(idAsesor, str):
            self.asesor = DBRef('empleado', ObjectId(idAsesor))
        elif isinstance(idAsesor, DBRef):
            self.asesor = idAsesor
        else:
            self.asesor = None
        self.fecha = fecha
        self.nombreCliente = nombre
        self.apellidoCliente = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.motivo = motivo
        self.estado = estado

