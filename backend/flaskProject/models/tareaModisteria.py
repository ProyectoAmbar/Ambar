from bson import DBRef, ObjectId

class tareaModisteria():
    def __init__(self, formmedidas, modista, producto,idFormulario, preciosCompletado: bool, completado: bool, fecha:str):
        if isinstance(formmedidas, str):
            self.formMedidas = DBRef('formatoMedidas', ObjectId(formmedidas))
        elif isinstance(formmedidas, DBRef):
            self.formMedidas = formmedidas

        if isinstance(modista, str):
            self.modista = DBRef('empleado', ObjectId(modista))
        elif isinstance(modista, DBRef):
            self.modista = modista
        else:
            self.modista = None

        if isinstance(idFormulario, str):
            self.formulario = DBRef('Producto', ObjectId(idFormulario))
        elif isinstance((idFormulario), DBRef):
            self.formulario = idFormulario
        else:
            self.formulario = None

        if isinstance(producto, str):
            self.producto = DBRef('Producto', ObjectId(producto))
        elif isinstance(producto, DBRef):
            self.producto = producto
        self.fecha = fecha
        self.preciosCompletado = preciosCompletado
        if preciosCompletado is False:
            self.completado = False
        elif preciosCompletado is True:
            self.completado = completado
