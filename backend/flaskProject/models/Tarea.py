from bson import ObjectId, DBRef

class Tarea():
    def __init__(self,idFormulario, idAsesor ,idProducto , fechaCitaDeMedidas, necesitaModista:bool ,estado:bool, cita1:bool, cita2:bool, cita3:bool):
        if isinstance(idFormulario, str):
            self.formulario = DBRef('formatoAlquiler', ObjectId(idFormulario))
        elif isinstance((idFormulario), DBRef):
            self.formulario = idFormulario
        else:
            self.formulario = None

        if isinstance(idAsesor,str):
            self.asesor = DBRef('empleado', ObjectId(idAsesor))
        elif isinstance(idAsesor,DBRef):
            self.asesor = idAsesor
        else:
            self.asesor = None

        if isinstance(idProducto, str):
            self.producto = DBRef('Producto', ObjectId(idProducto))
        elif isinstance((idProducto), DBRef):
            self.producto = idProducto
        else:
            self.producto = None
        self.fechaCitaDeMedidas = fechaCitaDeMedidas
        self.estado = estado
        self.cita1= cita1
        self.cita2 = cita2
        self.cita3 = cita3
        if estado is False:
            self.necesitaModista = False
        else:
            self.necesitaModista = necesitaModista


