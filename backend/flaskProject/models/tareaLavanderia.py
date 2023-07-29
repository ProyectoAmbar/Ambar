from bson import DBRef, ObjectId

class tareaLavanderia:
    def __init__(self, idLavanderia, idProducto, fecha:str, completado:bool):
        if isinstance(idLavanderia,str):
            self.lavanderia = DBRef('empleado', ObjectId(idLavanderia))
        elif isinstance(idLavanderia,DBRef):
            self.lavanderia = idLavanderia

        if isinstance(idProducto, str):
            self.producto = DBRef('Producto', ObjectId(idProducto))
        elif isinstance((idProducto), DBRef):
            self.producto = idProducto

        self.fecha = fecha
        self .completado = completado