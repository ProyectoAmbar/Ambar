from bson import DBRef, ObjectId

class tareaLavanderia:
    def __init__(self, idLavanderia, idProducto, idFormulario,fecha:str, completado:bool, postEntrega:bool):
        if isinstance(idLavanderia,str):
            self.lavanderia = DBRef('empleado', ObjectId(idLavanderia))
        elif isinstance(idLavanderia,DBRef):
            self.lavanderia = idLavanderia
        elif idLavanderia is None:
            self.lavanderia = None

        if isinstance(idProducto, str):
            self.producto = DBRef('Producto', ObjectId(idProducto))
        elif isinstance((idProducto), DBRef):
            self.producto = idProducto

        if isinstance(idFormulario, str):
            self.formulario = DBRef('Producto', ObjectId(idFormulario))
        elif isinstance((idFormulario), DBRef):
            self.formulario = idFormulario
        else:
            self.formulario = None

        self.fecha = fecha
        self .completado = completado
        self.postEntrega = postEntrega