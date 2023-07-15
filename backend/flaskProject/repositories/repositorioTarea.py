from repositories.interfaceRepositorio import interfaceRepositorio
from models.Tarea import Tarea
from bson import ObjectId,DBRef


class repositorioTareas(interfaceRepositorio[Tarea]):
    def save(self, infoTarea, estado):
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
        response['formulario'] = str(response['formulario'])
        response['asesor'] = str(response['asesor'])
        response['producto'] = str(response['producto'])

        return response

    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] = str(i['_id'])
            i['formulario'] = str(i['formulario'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        if response is not None:
            response['_id'] = str(response['_id'])
            response['formulario'] = str(response['formulario'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
        return response

    ##ID DE EMPLEADO##
    def getTareasPendientes(self,id):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"asesor": DBRef("empleado",ObjectId(id))}, {"estado": False}]}
        response = collection.find(query)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formulario'] = str(item['formulario'])
                item['asesor'] = str(item['asesor'])
                item['producto'] = str(item['producto'])
                allItems.append(item)
        return allItems


    def update(self, id, infoTarea):
        try:
            collection = self.db[self.collection]
            infoTarea = infoTarea.__dict__
            print(id)
            collection.update_one({"_id": ObjectId(id)}, {"$set": infoTarea})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['formulario'] = str(response['formulario'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
            return response
        except:
            return {"status": False,"code": 403,"message": "La tarea con id " + id + " no ha sido encontrada"}

    def getByIdToUpdate(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        return response

    def delete(self, id):
        dict = [{
            "status": True,
            "code": 202
        }]
        collection = self.db[self.collection]
        delObject = collection.delete_one({'_id': ObjectId(id)}).deleted_count
        dict.append({"deleted_count": delObject})
        return dict
