from bson import ObjectId, DBRef

class Tarea():
    def __init__(self,idFormulario:str, idAsesor:str ,idProducto:str , fechaCitaDeMedidas:str, necesitaModista:bool ,estado:bool):
        self.formulario = DBRef('formatoAlquiler', ObjectId(idFormulario))
        self.asesor = DBRef('empleado', ObjectId(idAsesor))
        self.producto = DBRef('Producto', ObjectId(idProducto))
        self.fechaCitaDeMedidas = fechaCitaDeMedidas
        self.estado = estado
        if estado is False:
            self.necesitaModista = False
        else:
            self.necesitaModista = necesitaModista


    def __init__(self,idFormulario:DBRef, idAsesor:DBRef ,idProducto:DBRef , fechaCitaDeMedidas:str, necesitaModista:bool ,estado:bool):
        self.formulario = idFormulario
        self.asesor = idAsesor
        self.producto = idProducto
        self.fechaCitaDeMedidas = fechaCitaDeMedidas
        self.estado = estado
        if estado is False:
            self.necesitaModista = False
        else:
            self.necesitaModista = necesitaModista