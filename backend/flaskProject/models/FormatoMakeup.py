from bson import ObjectId, DBRef
from datetime import datetime
class formatoMakeUP:
    def __init__(self, dia: int, mes: int, año:int, hora: int, minutos: int, fv: str, ref: str, tipo: str,nombreCliente: str, idMaquilladora,  entrega:str, direccion:str):
        self.fecha_hora = datetime(año,mes,dia,hora,minutos,0)
        self.fv = fv
        self.ref = ref
        self.tipo = tipo
        self.cliente = nombreCliente
        self.maquilladora = DBRef('empleado', ObjectId(idMaquilladora))
        self.entrega = entrega
        if self.entrega == "DOMICILIO":
            self.direccion = direccion
        elif self.entrega == "AMBAR":
            self.direccion = None
