from bson import ObjectId, DBRef
class tareaMakeup:
    def __init__(self, idMakeup, idFormMakeUp,referencia:str, tipoMakeup:str , fechaHora, completado:bool):
        if isinstance(idMakeup,str):
            self.idMakeup = DBRef('empleado', ObjectId(idMakeup))
        elif isinstance(idMakeup,DBRef):
            self.idMakeup = idMakeup
        elif idMakeup is None:
            self.idMakeup = None


        if isinstance(idFormMakeUp, str):
            self.formulario = DBRef('Producto', ObjectId(idFormMakeUp))
        elif isinstance((idFormMakeUp), DBRef):
            self.formulario = idFormMakeUp
        else:
            self.formulario = None
        self.referencia = referencia
        self.tipoMakeup = tipoMakeup
        self.fecha = fechaHora
        self .completado = completado
