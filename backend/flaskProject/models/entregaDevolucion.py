from bson import DBRef, ObjectId

class entregaDevolucion:
    def __init__(self, idProducto, idAsesor, idFormulario,fechaEntrega:str, entregaCompletado:bool, fechaDevolucion, devolucionCompletado:bool):
        if isinstance(idAsesor, str):
            self.asesor = DBRef('empleado', ObjectId(idAsesor))
        elif isinstance(idAsesor, DBRef):
            self.asesor = idAsesor
        else:
            self.asesor = None

        if isinstance(idProducto, str):
            self.producto = DBRef('Producto', ObjectId(idProducto))
        elif isinstance((idProducto), DBRef):
            self.producto = idProducto
        else:
            self.producto = None

        if isinstance(idFormulario, str):
            self.formulario = DBRef('formularioAlquiler', ObjectId(idFormulario))
        elif isinstance((idFormulario), DBRef):
            self.formulario = idFormulario
        else:
            self.formulario = None

        self.fechaEntrega = fechaEntrega
        self.entregaCompletado = entregaCompletado
        self.fechaDevolucion = fechaDevolucion
        if entregaCompletado is False:
            self.devolucionCompletado = False
        else:
            self.devolucionCompletado = devolucionCompletado
