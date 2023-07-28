from interfaceRepositorio import interfaceRepositorio
from bson import DBRef, ObjectId
from models.tareaLavanderia import tareaLavanderia

class repoLavanderia(interfaceRepositorio[tareaLavanderia]):
    def save(self, item: tareaLavanderia):
        dict = []
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['lavanderia'] = str(response['lavanderia'])
        response['producto'] = str(response['producto'])
        dict.append(response)
        return dict


    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['lavanderia'] = str(i['lavanderia'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
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