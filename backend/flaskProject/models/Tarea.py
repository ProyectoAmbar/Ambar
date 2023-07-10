from bson.objectid import ObjectId
class Tarea():
    def __init__(self, idAsesor, idEmpleado,idProducto,mensaje,estado,observaciones):
        self.asesor = ObjectId(idAsesor)
        if idEmpleado is not None:
            self.empleado = ObjectId(idEmpleado)
        else:
            self.empleado = idEmpleado
        self.producto = ObjectId(idProducto)
        self.mensaje = mensaje
        self.estado = estado
        self.observaciones = observaciones



