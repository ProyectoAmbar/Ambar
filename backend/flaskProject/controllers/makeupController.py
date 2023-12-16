from repositories.makeupRepo import makeupRepo
from repositories.repoTareaMakeUp import repoTareaMakeup
from models.FormatoMakeup import formatoMakeUP
from models.tareaMakeup import tareaMakeup
class makeupController():
    def __init__(self):
        self.repoMakeup = makeupRepo()
        self.repoTareaMakeup = repoTareaMakeup()

    def create(self, infoMakeup):
        try:
            if self.isValid(infoMakeup):
                dict = []
                if (infoMakeup['entrega'] == "DOMICILIO" and infoMakeup['direccion'] != None) or infoMakeup['entrega'] == "AMBAR":
                    search = self.repoMakeup.getByFactura(infoMakeup['numeroFactura'])
                    if search is None:
                        form = formatoMakeUP(infoMakeup['dia'] , infoMakeup['mes'] , infoMakeup['año'], infoMakeup['hora'] , infoMakeup['minutos'],
                        infoMakeup['numeroFactura'] , infoMakeup['referencia'], infoMakeup['tipo'] , infoMakeup['cliente'] , infoMakeup['maquilladora'], infoMakeup['entrega'],infoMakeup['direccion'])
                        response = self.repoMakeup.save(form)
                    else:
                        return {"status": False, "code": 400, "message": "Ya existe un registro con ese numero de factura"}
                    try:
                        if response['_id']:
                            tarea = tareaMakeup( form.maquilladora,response['_id'], form.ref, form.tipo, form.fecha_hora, False)
                            responseTarea = self.repoTareaMakeup.save(tarea)
                            dict.append(response)
                            dict.append(responseTarea)
                            return dict
                    except:
                         return {"status": False, "code": 400, "message": "No pudo ser agregado el Formulario de maquillaje"}
        except:
            return {"status": False, "code": 400, "message": "Por favor revise la información enviada"}
    def getAll(self):
        return self.repoMakeup.getAll()

    def getById(self, id):
        return self.repoMakeup.getById(id)

    def getByFactura(self, factura):
        return self.repoMakeup.getByFactura(factura)
    def updateMakeUpFom(self,id,infoUpdate):
        if self.isValid(infoUpdate):
            if ((infoUpdate['entrega'] == "DOMICILIO" and infoUpdate['direccion'] != None) or
                    infoUpdate['entrega'] == "AMBAR"):
                form = formatoMakeUP(infoUpdate['dia'], infoUpdate['mes'], infoUpdate['año'], infoUpdate['hora'],
                                     infoUpdate['minutos'],
                                     infoUpdate['numeroFactura'], infoUpdate['referencia'], infoUpdate['tipo'],
                                     infoUpdate['cliente'], infoUpdate['maquilladora'], infoUpdate['entrega'],
                                     infoUpdate['direccion'])
            return self.repoMakeup.update(id, form)

    def deleteMakeUpForm(self,id):
        return self.repoMakeup.delete(id)



    def isValid(self,infoMakeup):
        try:
            if(infoMakeup['dia']!= None and infoMakeup['mes']!= None and infoMakeup['año']!= None and infoMakeup['hora']!= None and
                          infoMakeup['minutos']!= None and
                          infoMakeup['numeroFactura']!= None and infoMakeup['referencia']!= None and infoMakeup['tipo']!= None and infoMakeup['cliente']!= None and
                          infoMakeup['maquilladora']!= None and infoMakeup['entrega']!= None):
                return True
        except:
            return False

