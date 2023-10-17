from bson import DBRef,ObjectId
from datetime import datetime

class auditoria:
    def __init__(self,idEmpleado, metodo, descripcion:str, cantidad):
        if isinstance(idEmpleado,str):
            self.empleado = DBRef('empleado', ObjectId(idEmpleado))
        elif isinstance(idEmpleado,DBRef):
            self.empleado = idEmpleado
        elif idEmpleado is None:
            self.empleado = None
        self.metodo = metodo
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.fecha_Hora = str(datetime.now())