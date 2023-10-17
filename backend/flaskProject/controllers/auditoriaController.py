from models.auditoria import auditoria
from repositories.repositorioAuditoria import repositorioAuditoria

class auditoriaController():
    def __init__(self):
        self.repoAuditoria = repositorioAuditoria()

    def create(self,infoAuditoria):
        try:
            audit = auditoria(infoAuditoria['empleado'], infoAuditoria['metodo'], infoAuditoria['descripcion'],infoAuditoria['saldo'])
            return self.repoAuditoria.save(audit)
        except:
            return {"status": False, "code": 400, "message": "no fue posible agregar un registro "}

    def getRegistroById(self, id):
        return self.repoAuditoria.getById(id)

    def getAllResgistro(self):
        return self.repoAuditoria.getAll()