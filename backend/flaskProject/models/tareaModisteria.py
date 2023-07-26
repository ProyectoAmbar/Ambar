from bson import DBRef, ObjectId

class tareaModisteria():
    def __init__(self, formmedidas, modista, producto, preciosCompletado: bool, completado: bool, fecha:str):
        if isinstance(formmedidas, str):
            self.formMedidas = DBRef('formatoMedidas', ObjectId(formmedidas))
        else:
            self.formMedidas = formmedidas

        if isinstance(modista, str):
            self.modista = DBRef('empleado', ObjectId(modista))
        else:
            self.modista = modista

        if isinstance(producto, str):
            self.producto = DBRef('Producto', ObjectId(producto))
        else:
            self.producto = producto
        self.fecha = fecha
        self.preciosCompletado = preciosCompletado
        if preciosCompletado is False:
            self.completado = False
        elif preciosCompletado is True:
            self.completado = completado
