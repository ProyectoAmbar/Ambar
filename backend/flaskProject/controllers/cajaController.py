from models.caja import caja
from models.auditoria import auditoria
from repositories.cajaRepository import repoCaja
from repositories.repositorioAuditoria import repositorioAuditoria

from datetime import date, datetime

class cajaController():
    def __init__(self):
        self.repoCaja = repoCaja()
        self.repoAuditoria = repositorioAuditoria()

    def Create(self):
        info = caja(0)
        response = self.repoCaja.save(info)
        return response

    def restaurarSaldo(self):
        dict = []
        infoCaja = caja(0)
        getCaja = self.repoCaja.getOne()
        dict.append(self.repoCaja.update(getCaja['_id'], infoCaja))
        registro = auditoria(None,"Retiro Automatico", "Se realiza retiro automatico de caja", getCaja['saldo'])
        dict.append(self.repoAuditoria.save(registro))
        return dict

    def agregarSaldo(self,infoSaldo):
        dict = []
        infoCaja = self.repoCaja.getOne()
        cajaUpdate = caja( infoCaja['saldo'] + infoSaldo['saldo'])
        dict.append( self.repoCaja.update(infoCaja['_id'],cajaUpdate))
        registro = auditoria(infoSaldo['empleado'],"Deposito", infoSaldo['descripcion'],infoSaldo['saldo'])
        dict.append(self.repoAuditoria.save(registro))
        return dict


    def retirarSaldo(self,infoSaldo):
        infoCaja = self.repoCaja.getOne()
        if infoSaldo['saldo'] <= infoCaja['saldo'] and infoSaldo['saldo'] >= 0:
            dict = []
            cajaUpdate = caja(infoCaja['saldo'] - infoSaldo['saldo'])
            dict.append( self.repoCaja.update(infoCaja['_id'], cajaUpdate))
            registro = auditoria(infoSaldo['empleado'], "retiro", infoSaldo['descripcion'], infoSaldo['saldo'])
            dict.append(self.repoAuditoria.save(registro))
            return dict
        else:
            return {"status": False, "code":400, "message": "el saldo a retirar es mayor a la cantidad disponible en caja"}

    def verSaldo(self):
        return self.repoCaja.getOne()




