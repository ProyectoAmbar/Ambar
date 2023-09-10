from models.FormatoMedidas import formatoMedidas
from repositories.repositorioFormMedidas import repositorioFormMedidas

class fomMedidasController():
    def __init__(self):
        self.repoMedidas = repositorioFormMedidas()


    def create(self,infoMedidas):
        if self.isValid(infoMedidas):
            if infoMedidas['necesitaArreglos'] is True:
                for arreglo in infoMedidas['arreglos']:
                    if (arreglo['mensaje'] is None  or arreglo['cm'] is None):
                        return {"status": False, "code": 400, "message": "se necesitan los arreglos"}
            form = formatoMedidas(infoMedidas['asesor'],infoMedidas['formulario'],infoMedidas['producto'],
            infoMedidas['arreglos'],infoMedidas['estadoCita'],infoMedidas['necesitaArreglos'])
            return self.repoMedidas.save(form)

    def getAll(self):
        return self.repoMedidas.getAll()

    def getById(self, id):
        return self.repoMedidas.getById(id)

    def getByFoorm(self, idFormularioAlquiler):
        return self.repoMedidas.getFormMedidasByFormAlquiler(idFormularioAlquiler)
    def UpdateForm(self,id,infoMedidas):
        search = self.repoMedidas.getByIdToUpdate(id)
        if self.isValid(infoMedidas) and search is not None:
            if infoMedidas['necesitaArreglos'] is True:
                for arreglo in infoMedidas['arreglos']:
                    if (arreglo['mensaje'] is None  or arreglo['cm'] is None):
                        return {"status": False, "code": 400, "message": "se necesitan los arreglos"}
            form = formatoMedidas(infoMedidas['asesor'],infoMedidas['formulario'],infoMedidas['producto'],
            infoMedidas['arreglos'],infoMedidas['estadoCita'],infoMedidas['necesitaArreglos'])
            return self.repoMedidas.update(id,form)
        else:
            return {"status": False, "code": 400, "message": "hace falta información para actualizar el formato de medidas"}

    def responderFormMedidas(self,id,infoMedidas):
        try:
            search = self.repoMedidas.getByIdToUpdate(id)
            arreglos = search['arreglos']
            if len(arreglos) == len(infoMedidas['arreglos']):
                for i in range(len(arreglos)):
                    print(i)
                    print(arreglos[i]["precio"])
                    search['arreglos'][i]["precio"] = infoMedidas["arreglos"][i]["precio"]
                    print(search)
                form = formatoMedidas(search['asesor'], search['formulario'], search['producto'],
                search['arreglos'], search['estadoCita'], True)
                return self.repoMedidas.update(id,form)
            else:
                return {"status":False, "code": 400, "message": "hacen falta arreglos por proporcionar"}
        except:
            return {"status": False, "code": 400, "message": "No se encontro el id"}









    def deleteForm(self,id):
        search = self.repoMedidas.getById(id)
        if search is not None:
            return self.repoMedidas.delete(id)
        else:
            return {"status": False, "code": 400, "message": "No se econtro el id" + id}






    def isValid(self, infoMedidas):
        try:
            if (infoMedidas['asesor'] != None and infoMedidas['formulario'] != None and infoMedidas['producto']!= None
            and infoMedidas['estadoCita'] != None and infoMedidas['necesitaArreglos'] != None):
                return True
        except:
            return False

