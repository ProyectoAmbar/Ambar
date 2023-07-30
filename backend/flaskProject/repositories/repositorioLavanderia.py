from repositories.interfaceRepositorio import interfaceRepositorio
from bson import DBRef, ObjectId
from models.tareaLavanderia import tareaLavanderia

class repoLavanderia(interfaceRepositorio[tareaLavanderia]):
    def save(self, item: tareaLavanderia):

        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        if response['lavanderia'] is not None:
            response['lavanderia'] = str(response['lavanderia'])
        response['producto'] = str(response['producto'])

        return response


    def getAll(self):

        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            if response['lavanderia'] is not None:
                i['lavanderia'] = str(i['lavanderia'])
            i['producto'] = str(i['producto'])
            allItems.append(i)

        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            if response['lavanderia'] is not None:
                response['lavanderia'] = str(response['lavanderia'])
            response['producto'] = str(response['producto'])
        return response

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        return response
    def update(self,id , item:tareaLavanderia):
        try:
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            if response['lavanderia'] is not None:
                response['lavanderia'] = str(response['lavanderia'])
            response['producto'] = str(response['producto'])
            return response
        except:
            dict = [{
                "status": False,
                "code": 403,
                "message": "El candidato con id "+id+" no ha sido encontrado"
            }]
            return dict


    def delete(self,id):
        dict = [{
            "status": True,
            "code": 202
        }]
        collection = self.db[self.collection]
        delObject = collection.delete_one({'_id':ObjectId(id)}).deleted_count
        dict.append({"deleted_count": delObject})
        return dict

    def getTareasAllPendientes(self):
        allItems = []
        collection = self.db[self.collection]
        query = {"completado": False}
        response = collection.find(query).sort("fecha",1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                if item['lavanderia'] is not None:
                    item['lavanderia'] = str(item['lavanderia'])
                item['producto'] = str(item['producto'])
                allItems.append(item)
        return allItems

    def getAlltareasPendientesLavanderia(self,idLavanderia):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"completado": False}, {"lavanderia": DBRef('empleado',ObjectId(idLavanderia))}]}
        response = collection.find(query).sort("fecha", 1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                if item['lavanderia'] is not None:
                    item['lavanderia'] = str(item['lavanderia'])
                item['producto'] = str(item['producto'])
                allItems.append(item)
        return allItems

    def getTareasSinAsignar(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"lavanderia": None})
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                if item['lavanderia'] is not None:
                    item['lavanderia'] = str(item['lavanderia'])
                item['producto'] = str(item['producto'])
                allItems.append(item)
        return allItems


