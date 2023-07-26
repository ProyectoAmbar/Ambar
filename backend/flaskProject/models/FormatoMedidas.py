from bson import ObjectId, DBRef
from bson import DBRef,ObjectId

class formatoMedidas():
    def __init__(self,asesor:str,formulario:str,producto:str ,arreglos, estadoCita:bool, necesitaArreglos:bool):
        self.asesor = DBRef('empleado', ObjectId(asesor))
        self.formulario = DBRef('formatoAlquiler', ObjectId(formulario))
        self.producto = DBRef('Producto', ObjectId(producto))
        self.estadoCita = estadoCita
        if necesitaArreglos is False:
            self.arreglos = None
        else:
            self.arreglos = arreglos

    def __init__(self,asesor:DBRef,formulario:DBRef,producto:DBRef ,arreglos, estadoCita:bool, necesitaArreglos:bool):
        self.asesor = asesor
        self.formulario = formulario
        self.producto = producto
        self.estadoCita = estadoCita
        if necesitaArreglos is False:
            self.arreglos = None
        else:
            self.arreglos = arreglos

