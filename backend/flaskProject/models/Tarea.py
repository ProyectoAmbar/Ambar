from bson import ObjectId, DBRef

class Tarea():
    def __init__(self,idFormulario:str, idAsesor:str ,idProducto:str , fechaCitaDeMedidas:str, necesitaModista:bool ,estado:bool):
        self.formulario = DBRef('formatoAlquiler', ObjectId(idFormulario))
        self.asesor = DBRef('empleado', ObjectId(idAsesor))
        self.producto = DBRef('producto', ObjectId(idProducto))
        self.fechaCitaDeMedidas = fechaCitaDeMedidas
        self.necesitaModista = necesitaModista
        self.estado = estado