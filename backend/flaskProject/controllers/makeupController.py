from repositories.makeupRepo import makeupRepo
from models.FormatoMakeup import formatoMakeUP
class makeupController():
    def __init__(self):
        self.repoMakeup = makeupRepo()
    def create(self, infoMakeup):
        if self.isValid(infoMakeup):
            if infoMakeup['entrega'] is "DOMICILIO" and infoMakeup['direccion'] != None:
                form = formatoMakeUP(infoMakeup['dia'] , infoMakeup['mes'] , infoMakeup['año'], infoMakeup['hora'] , infoMakeup['minutos'],
                infoMakeup['fv'] , infoMakeup['ref'], infoMakeup['tipo'] , infoMakeup['cliente'] , infoMakeup['maquilladora'], infoMakeup['entrega'],infoMakeup['direccion'])
                response = self.repoMakeup.save(form)
                return response
    def getAll(self):
        return self.repoMakeup.getAll()

    def getById(self, id):
        return self.repoMakeup.getById(id)

    def getByFactura(self, factura):
        return self.repoMakeup.getByFactura(factura)
    def updateMakeUpFom(self,id,infoUpdate):
        if self.isValid(infoUpdate):
            form = formatoMakeUP(infoUpdate['dia'], infoUpdate['mes'], infoUpdate['año'], infoUpdate['hora'],
                                 infoUpdate['minutos'],
                                 infoUpdate['fv'], infoUpdate['ref'], infoUpdate['tipo'], infoUpdate['cliente'],
                                 infoUpdate['maquilladora'], infoUpdate['entrega'], infoUpdate['direccion'])
            return self.updateMakeUpFom(id,form)

    def deleteMakeUpForm(self,id):
        return self.repoMakeup.delete(id)



    def isValid(self,infoMakeup):
        try:
            if(infoMakeup['dia']!= None and infoMakeup['mes']!= None and infoMakeup['año']!= None and infoMakeup['hora']!= None and
                          infoMakeup['minutos']!= None and
                          infoMakeup['fv']!= None and infoMakeup['ref']!= None and infoMakeup['tipo']!= None and infoMakeup['cliente']!= None and
                          infoMakeup['maquilladora']!= None and infoMakeup['entrega']!= None):
                return True
        except:
            return False

