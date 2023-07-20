from repositories.repositorioTarea import repositorioTareas
from models.producto import Producto
from repositories.repositorioFormMedidas import repositorioFormMedidas
from repositories.repositorioTareaModista import repoTareaModista
from models.Tarea import Tarea
from models.FormatoMedidas import formatoMedidas
from models.tareaModisteria import tareaModisteria


def desbloquearProducto(self, id):
    search = self.RepositorioProductos.getById(id)
    try:
        if search['disponible'] is False:
            productoUpdate = {
                "nombre": search['nombre'],
                "referencia": search['referencia'],
                "imagenProducto": search['imagenProducto'],
                "color": search['color'],
                "disponible": True
            }
    except:
        return {"status": False, "code": 400, "message": "No se encontro el producto de id" + id}


class tareaController():
    def __init__(self):
        self.repositorioTareas = repositorioTareas()
        self.repoModista = repoTareaModista()
        self.repoFormMedidas = repositorioFormMedidas()

    def Create(self, infoTarea):
        print("crear tarea")
        if (infoTarea['formulario'] != None and infoTarea['producto'] != None and infoTarea['asesor']!=None and
            infoTarea['estado'] != None and infoTarea['fechaCitaDeMedidas'] != None and infoTarea['necesitaModista']!=None):
            tarea = Tarea(infoTarea['formulario'], infoTarea['asesor'],infoTarea['producto'],
                           infoTarea['fechaCitaDeMedidas'], infoTarea['necesitaModista'],infoTarea['estado'])
            return self.repositorioTareas.save(tarea, infoTarea['estado'])
        else:
            return {"status": False, "code": 400, "message": "no se tiene la información necesaria para crear la tarea"}

    def getAllTareas(self):
        print("get all tareas")
        return self.repositorioTareas.getAll()

    def getById(self, _id):
        print("get producto by id")
        response = self.repositorioTareas.getById(_id)
        if response != None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No se encontro la tarea con id: " + _id}

    def Update(self, id, infoUpdate):
        print("actualizar Tarea")
        search = self.repositorioTareas.getById(id)
        if search is not None and (infoUpdate['formulario'] != None and infoUpdate['producto'] != None and infoUpdate['asesor'] != None and
            infoUpdate['estado'] != None and infoUpdate['fechaCitaDeMedidas'] != None and infoUpdate['necesitaModista'] != None):
            response = self.repositorioTareas.update(id, Tarea(infoUpdate['formulario'], infoUpdate['producto'], infoUpdate['asesor'],
                          infoUpdate['estado'], infoUpdate['fechaCitaDeMedidas'], infoUpdate['necesitaModista']))

            response.append({"status": True, "code": 200, "message": "La tarea fue actualizada"})
            return response
        else:
            return {"status": False, "code": 400, "message": "Hace falta informacion para actualizar el producto"}

    def responderTareaC(self, id, infoUpdate, estado):
        dict = []
        search = self.repositorioTareas.getByIdToUpdate(id)
        if search is not None and (infoUpdate['estado'] is True and infoUpdate['necesitaModista'] is True):
            tarea = Tarea(search['formulario'],search['asesor'], search['producto'], search['fechaCitaDeMedidas'],True,True)
            if infoUpdate['arreglos'] is not None or len(infoUpdate['arreglos']) > 0:
                response = self.repositorioTareas.update(id, tarea)
                formMedida = formatoMedidas(search['asesor'],search['formulario'],search['producto'],infoUpdate['arreglos'],True,True)
                responseFormMedida = self.repoFormMedidas.save(formMedida)
                tareaModista = tareaModisteria(responseFormMedida['_id'], None, search['producto'],False, False)
                responseTareaModista = self.repoModista.save(tareaModista)
                dict.append(response)
                dict.append(responseFormMedida)
                dict.append(responseTareaModista)
                return dict
            else:
                return {"status": False, "code": 400, "message": "Se necesitan los arreglos a realizar"}
        elif search is not None and(infoUpdate['estado'] != None and infoUpdate['necesitaModista'] != None):
            tarea = Tarea(search['formulario'], search['asesor'], search['producto'], search['fechaCitaDeMedidas'], infoUpdate['necesitaModista'], infoUpdate['estado'])
            return self.repositorioTareas.update(id,tarea)
        else:
            return {"status": False, "code": 400, "message": "No se encontro la tarea a responder"}

    def verTareasPendientesPorAsesor(self, id):
        search = self.repositorioTareas.getTareasPendientesPorAsesor(id)
        return search

    def getAllTareasPendientes(self):
        return self.repositorioTareas.getAllTareasPendientes()

    def Delete(self, id):
        print("eliminar un producto")
        return self.repositorioTareas.delete(id)
