from datetime import date
from bson import ObjectId, DBRef
import pymongo

class formatoAlquiler():
    def __init__(self, nombre: str, apellido:str, correo:str, celular:str,direccion:str,idAsesor, sede:str, idProducto, identificacion, AñoEntrega, MesEntrega, DiaEntrega, NumeroDeFactura, accesorio, velo, aro, metodoDePago, Abono, Saldo, Deposito, AñoCitaMedidas, MesCitaMedidas,DiaCitaMedidas):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.celular = celular
        self.direccion = direccion
        self.asesor = DBRef("empleado", ObjectId(idAsesor))
        self.sede = sede
        self.Producto = DBRef("Producto", ObjectId(idProducto))
        self.identificacion = identificacion
        self.fechaDeFactura = str(date.today())
        self.fechaDeEntrega = str(date(AñoEntrega, MesEntrega, DiaEntrega))
        self.numeroFactura = NumeroDeFactura
        self.accesorio = accesorio
        self.velo = velo
        self.aro = aro
        self.total = Saldo + Deposito
        self.metodoDePago = metodoDePago
        self.abono = Abono
        self.saldo = Saldo
        self.deposito = Deposito
        self.FechaCitaDeMedidas = str(date(AñoCitaMedidas,MesCitaMedidas,DiaCitaMedidas))



