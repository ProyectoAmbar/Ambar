from repositories.interfaceRepositorio import interfaceRepositorio
from models.Tarea import Tarea
from bson.objectid import ObjectId


class repositorioTareas():
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

    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            if i['empleado'] != None:
                i['empleado'] = str(i['empleado'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        dict = []
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        response['producto'] = str(response['producto'])
        if response['empleado'] != None:
            response['empleado'] = str(response['empleado'])
        dict.append(response)
        return dict

    def update(self, id, infoTarea):
        try:
            dict = []
            collection = self.db[self.collection]
            infoTarea = infoTarea.__dict__
            print(id)
            collection.update_one({"_id": ObjectId(id)}, {"$set": infoTarea})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
            if response['empleado'] is not None:
                response['empleado'] = str(response['empleado'])
            dict.append(response)
            return dict
        except:
            dict = [{
                "status": False,
                "code": 403,
                "message": "La tarea con id " + id + " no ha sido encontrada"
            }]
            return dict

    def delete(self, id):
        dict = [{
            "status": True,
            "code": 202
        }]
        collection = self.db[self.collection]
        delObject = collection.delete_one({'_id': ObjectId(id)}).deleted_count
        dict.append({"deleted_count": delObject})
        return dict
