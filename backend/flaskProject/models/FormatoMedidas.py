from bson import ObjectId, DBRef
from bson import DBRef,ObjectId

class formatoMedidas():
    def __init__(self,asesor,formulario,producto ,arreglos, estadoCita, necesitaArreglos):
        self.asesor = DBRef('empleado', ObjectId(asesor))
        self.formulario = DBRef('formulario', ObjectId(formulario))
        self.producto = DBRef('producto', ObjectId(producto))
        self.estadoCita = estadoCita
        if necesitaArreglos is False:
            self.arreglos = None
        else:
            self.arreglos = arreglos

