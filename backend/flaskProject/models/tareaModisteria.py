from bson import DBRef, ObjectId

class tareaModisteria():
    def __init__(self, modista, producto, mensaje, arreglos, completado):
        self.modista = DBRef('empleado', ObjectId(modista))
        self.producto = DBRef('Producto', ObjectId(producto))
        self.mensaje = mensaje
        self.arreglos = arreglos
        self.completado = completado