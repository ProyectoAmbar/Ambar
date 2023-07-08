from bson.objectid import ObjectId
class Tarea():
    def __init__(self, idAsesor, idEmpleado,idProducto,mensaje,estado,observaciones):
        self.asesor = ObjectId(idAsesor)
        self.empleado = ObjectId(idEmpleado)
        self.producto = ObjectId(idProducto)
        self.mensaje = mensaje
        self.estado = estado
        self.observaciones = observaciones



