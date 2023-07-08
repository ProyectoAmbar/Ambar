from datetime import date
from bson.objectid import ObjectId
import pymongo

class formatoAlquiler():
    def __init__(self, idAsesor, idProducto, idCliente, identificacion, AñoFactura,MesFactura,DiaFactura, NumeroDeFactura, accesorio, corbatin, velo, aro, total, metodoDePago, Abono, Saldo, Deposito, AñoCitaMedidas, MesCitaMedidas,DiaCitaMedidas):
        self.asesor = ObjectId(idAsesor)
        self.Producto = ObjectId(idProducto)
        self.Cliente = ObjectId(idCliente)
        self.identificacion = identificacion
        self.fechaDeFactura = str(date(AñoFactura, MesFactura, DiaFactura))
        self.numeroFactura = NumeroDeFactura
        self.accesorio = accesorio
        self.corbatin = corbatin
        self.velo =  velo
        self. aro = aro
        self.total = total
        self.metodoDePago = metodoDePago
        self.abono = Abono
        self.saldo = Saldo
        self.deposito = Deposito
        self.FechaCitaDeMedidas = str(date(AñoCitaMedidas,MesCitaMedidas,DiaCitaMedidas))



