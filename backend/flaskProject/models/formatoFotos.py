from models.abstractModel import AbstractModel
from datetime import datetime
class formatoFotos():
    def __init__(self,fecha,fv:str,locacion:str,referencia:str, nombreCliente:str,numeroCliente:str,correoCliente:str, estado):
        self.nombreCliente = nombreCliente
        self.numeroCliente = numeroCliente
        self.correoCliente = correoCliente
        self.fv = fv
        self.fecha = fecha
        self.referencia = referencia
        self.locacion = locacion
        self.estado = estado