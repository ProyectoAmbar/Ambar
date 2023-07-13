from datetime import date
from bson import ObjectId, DBRef
import pymongo

class formatoAlquiler():
    def __init__(self, idAsesor, idProducto, identificacion, AñoEntrega, MesEntrega, DiaEntrega, NumeroDeFactura, accesorio, corbatin, velo, aro, total, metodoDePago, Abono, Saldo, Deposito, AñoCitaMedidas, MesCitaMedidas,DiaCitaMedidas):
        self.asesor = DBRef("empleado", ObjectId(idAsesor))
        self.Producto = DBRef("producto", ObjectId(idProducto))
        self.identificacion = identificacion
        self.fechaDeFactura = str(date.today())
        self.fechaDeEntreta = str(date(AñoEntrega, MesEntrega, DiaEntrega))
        self.numeroFactura = NumeroDeFactura
        self.accesorio = accesorio
        self.corbatin = corbatin
        self.velo = velo
        self. aro = aro
        self.total = total
        self.metodoDePago = metodoDePago
        self.abono = Abono
        self.saldo = Saldo
        self.deposito = Deposito
        self.FechaCitaDeMedidas = str(date(AñoCitaMedidas,MesCitaMedidas,DiaCitaMedidas))



