from controllers.fotosController import fotosController
from controllers.makeupController import makeupController

def isValid(infoFotoMake):

    try:
        if(infoFotoMake['diaMakeUp'] and infoFotoMake['mesMakeUp'] and infoFotoMake['añoMakeUp'] and infoFotoMake['horaMakeUp']
                and infoFotoMake['minutosMakeUp'] and infoFotoMake['fvMakeUp'] and infoFotoMake['refMakeUp'] and infoFotoMake['entregaMakeUp']
                and infoFotoMake['direccionMakeUp'] and infoFotoMake['tipoMakeUp'] and infoFotoMake['nombreCliente'] and 'correoCliente' and 'numeroCliente' and infoFotoMake['maquiladdoraMakeUp'] and infoFotoMake['direccionMakeUp'] and
                infoFotoMake['diaFoto'] and infoFotoMake['mesFoto'] and infoFotoMake['añoFoto'] and
                infoFotoMake['horaFoto'] and infoFotoMake['minutoFoto']and infoFotoMake['fvFoto'] and infoFotoMake['locacionFoto']
                and infoFotoMake['refFoto']):

            return True
    except:
        return False
class fotoMakeUpController:
    def __init__(self):
        self.foto = fotosController()
        self.makeUp = makeupController()

    def createFotoMakeUp(self, infoFotoMake):
        try:
            infoMakeup = {
                "referencia": infoFotoMake['refMakeUp'],
                "tipo": infoFotoMake['tipoMakeUp'],
                "numeroFactura": infoFotoMake['fvMakeUp'],
                "entrega": infoFotoMake['entregaMakeUp'],
                "cliente": infoFotoMake['nombreClienteMakeUp'],
                "direccion": infoFotoMake['direccionMakeUp'],
                "maquilladora": infoFotoMake['maquilladoraMakeUp'],
                "dia": infoFotoMake['diaMakeUp'],
                "mes": infoFotoMake['mesMakeUp'],
                "año": infoFotoMake['añoMakeUp'],
                "hora": infoFotoMake['horaMakeUp'],
                "minutos": infoFotoMake['minutosMakeUp']
            }

            infoFoto = {
                "nombreCliente": infoFotoMake['nombreCliente'],
                "numeroCliente": infoFotoMake['numeroCliente'],
                "correoCliente": infoFotoMake['correoCliente'],
                "dia": infoFotoMake['diaFoto'],
                "mes": infoFotoMake['mesFoto'],
                "año": infoFotoMake['añoFoto'],
                "hora": infoFotoMake['horaFoto'],
                "minutos": infoFotoMake['minutoFoto'],
                "fv": infoFotoMake['fvFoto'],
                "referencia": infoFotoMake['refFoto'],
                "locacion": infoFotoMake['locacionFoto']
            }
            dict = []
            responseFoto = self.foto.create(infoFoto)
            responseMakeUp = self.makeUp.create(infoMakeup)
            dict.append(responseFoto)
            dict.append(responseMakeUp)
            return dict
        except:
            return {"status":False, "code": 400, "message": "Por Favor revise la información ingresada"}