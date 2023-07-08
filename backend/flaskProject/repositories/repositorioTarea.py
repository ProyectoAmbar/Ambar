from repositories.interfaceRepositorio import interfaceRepositorio
from models.Tarea import Tarea
from bson.objectid import ObjectId

class repositorioTareas(interfaceRepositorio[Tarea]):
    def save(self, infoTarea, estado):
        dict = []
        print(infoTarea.estado)
        infoTarea.estado = estado
        print("def save")
        collection = self.db['Tarea']
        inserted = collection.insert_one(infoTarea.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        print(response)
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        response['producto'] = str(response['producto'])
        if response['empleado'] != None:
            response['empleado'] = str(response['empleado'])
        dict.append(response)
        return dict
    pass