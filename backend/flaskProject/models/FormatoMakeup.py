from bson import ObjectId, DBRef
from datetime import datetime
class formatoMakeUP:
    def __init__(self, dia: int, mes: int, año:int, hora: int, minutos: int, fv: int, ref: str, tipo: str,nombreCliente: str, idMaquilladora,  entrega:str, direccion:str):
        self.FECHAHORA = datetime(año,mes,dia,hora,minutos,0)
        self.fv = fv
        self.ref = ref
        self.tipo = tipo
        self.cliente = nombreCliente
        self.maquilladora = DBRef('empleado', ObjectId(idMaquilladora))
        self.entrega = entrega
        if self.entrega is "DOMICILIO":
            self.direccion = direccion
        elif self.entrega is "AMBAR":
            self.direccion = None
