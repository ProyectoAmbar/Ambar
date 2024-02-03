from models.abstractModel import AbstractModel
from datetime import datetime
class formatoFotos():
    def __init__(self, dia:int, mes:int,año:int,hora:int,minutos:int,fv:str,locacion:str,referencia:str, nombreCliente:str,numeroCliente:str,correoCliente:str):
        self.nombreCliente = nombreCliente
        self.numeroCliente = numeroCliente
        self.correoCliente = correoCliente
        self.fecha = datetime(año,mes,dia,hora,minutos,0)
        self.fv = fv
        self.referencia = referencia
        self.locacion = locacion
        self.estado = False

    def __init__(self, fecha:str, fv:str,locacion:str,referencia:str, nombreCliente:str,numeroCliente:str,correoCliente:str, estado:bool):
        self.nombreCliente = nombreCliente
        self.numeroCliente = numeroCliente
        self.correoCliente = correoCliente
        self.fecha = fecha
        self.fv = fv
        self.referencia = referencia
        self.locacion = locacion
        self.estado = estado


