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
        response['idFormMakeup'] = str(response['idFormMakeup'])
        dict.append(response)
        return dict


    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['idMakeup'] = str(i['idMakeup'])
            i['idFormMakeup'] = str(i['idFormMakeup'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['idFormMakeup'] = str(response['idFormMakeup'])
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
            response['idFormMakeup'] = str(response['idFormMakeup'])
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

    def getAllMakeupSinAsignar(self):
        collection = self.db[self.collection]
        response = collection.find_one({"idMakeup": None })
        if response != None:
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['idFormMakeup'] = str(response['idFormMakeup'])
        return response

    def getAllPendientes(self):
        collection = self.db[self.collection]
        response = collection.find({"completado": False}).sort("fecha", 1)
        if response != None:
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['idFormMakeup'] = str(response['idFormMakeup'])
        return response

    def getAllPendientesByStylist(self,idMakeup):
        collection = self.db[self.collection]
        query = {"$and": [{"completado": False}, {"modista": DBRef('empleado', ObjectId(idMakeup))}]}
        response = collection.find(query).sort("fecha",1)
        if response != None:
            response['_id'] = str(response['_id'])
            response['idMakeup'] = str(response['idMakeup'])
            response['idFormMakeup'] = str(response['idFormMakeup'])
        return response

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": id})
        return response
