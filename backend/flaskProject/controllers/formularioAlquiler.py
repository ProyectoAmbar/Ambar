from models.FormatoAlquiler import formatoAlquiler
from models.Tarea import Tarea
from repositories.repositorioFormatoAlquiler import repositorioFormatoAlquiler
from repositories.repositorioTarea import repositorioTareas

class formularioAlquilerController():
    def __init__(self):
        self.repositorioAlquiler = repositorioFormatoAlquiler()
        self.repoTareas = repositorioTareas()

    def create(self, infoAlquiler):
        if self.isValid(infoAlquiler):
            formulario = formatoAlquiler(infoAlquiler['idAsesor'] , infoAlquiler['idProducto'] , infoAlquiler['idCliente'] , infoAlquiler['identificacion'] , infoAlquiler['AñoFactura'] , infoAlquiler['MesFactura'] ,
            infoAlquiler['DiaFactura'] , infoAlquiler['NumeroDeFactura'] , infoAlquiler['accesorio'] , infoAlquiler['corbatin'] , infoAlquiler['velo']  , infoAlquiler['aro'] , infoAlquiler['total'] ,
            infoAlquiler['metodoDePago'] , infoAlquiler['Abono'] , infoAlquiler['Saldo'] , infoAlquiler['Deposito'] , infoAlquiler['AñoCitaMedidas'] , infoAlquiler['MesCitaMedidas'] , infoAlquiler['DiaCitaMedidas'])
            print(formulario)
            dict = []
            response = self.repositorioAlquiler.save(formulario)
            print(response)
            dict.append(response)
            tareaInfo = Tarea(infoAlquiler['idAsesor'], None, infoAlquiler['idProducto'], None, None, False)

            responseTarea = self.repoTareas.save(tareaInfo, False);
            dict.append(responseTarea)
            return dict
        else:
            return {"status": False, "code": 400, "message": "el formulario no pudo ser creado"}



    def isValid(self, infoAlquiler):
        if (infoAlquiler['idAsesor'] and infoAlquiler['idProducto'] and infoAlquiler['idCliente'] and infoAlquiler['identificacion']
            and infoAlquiler['AñoFactura'] and infoAlquiler['MesFactura'] and infoAlquiler['DiaFactura'] and infoAlquiler['NumeroDeFactura']
            and infoAlquiler['accesorio'] != None and infoAlquiler['corbatin'] != None and infoAlquiler['velo'] != None and infoAlquiler['aro'] != None
            and infoAlquiler['total'] and infoAlquiler['metodoDePago'] and infoAlquiler['Abono'] and infoAlquiler['Saldo'] and infoAlquiler['Deposito']
            and infoAlquiler['AñoCitaMedidas'] and infoAlquiler['MesCitaMedidas'] and infoAlquiler['DiaCitaMedidas']):
            return True
        else:
            return False
