from bson import ObjectId, DBRef
from models.tareaMakeup import tareaMakeup
from repositories.interfaceRepositorio import interfaceRepositorio
class repoTareaMakeup(interfaceRepositorio[tareaMakeup]):
    def save(self, item:tareaMakeup):
        dict = []
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['idMakeup'] = str(response['idMakeup'])
        response['formulario'] = str(response['formulario'])
        dict.append(response)
        return dict

    def getCompletedTask(self,id):
        allItems = []
        collection = self.db[self.collection]
        print({"$and": [{"asesor": DBRef("empleado", ObjectId(id))}, {"estado": True}, {"necesitaModista": False}]})
        response = collection.find({"$and": [{"idMakeup": DBRef("empleado", ObjectId(id))}, {"completado": True}]})
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['idMakeup'] = str(item['idMakeup'])
                item['formulario'] = str(item['formulario'])
                allItems.append(item)
        return allItems

    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['idMakeup'] = str(i['idMakeup'])
            i['formulario'] = str(i['formulario'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['formulario'] = str(response['formulario'])
        return response
    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['formulario'] = str(response['formulario'])
        return response
    def update(self,id , item:tareaMakeup):
        try:
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['formulario'] = str(response['formulario'])
            return response
        except:
            dict = [{
                "status": False,
                "code": 403,
                "message": "El candidato con id "+id+" no ha sido encontrado"
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



    def getAllPendientes(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"completado": False}).sort("fecha", 1)
        if response != None:
            for i in response:
                i['_id'] = str(i['_id'])
                i['idMakeup'] = str(i['idMakeup'])
                i['formulario'] = str(i['formulario'])
                allItems.append(i)
        return allItems

    def getAllPendientesByStylist(self,idMakeup):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"completado": False}, {"idMakeup": DBRef('empleado', ObjectId(idMakeup))}]}
        response = collection.find(query).sort("fecha",1)
        if response != None:
            for i in response:
                i['_id'] = str(i['_id'])
                i['idMakeup'] = str(i['idMakeup'])
                i['formulario'] = str(i['formulario'])
                allItems.append(i)
        return allItems

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        return response
