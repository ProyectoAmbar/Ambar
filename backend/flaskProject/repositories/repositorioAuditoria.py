from repositories.interfaceRepositorio import interfaceRepositorio
from models.auditoria import auditoria
from bson import ObjectId

class repositorioAuditoria(interfaceRepositorio[auditoria]):
    def save(self, auditoriaInfo):
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(auditoriaInfo.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        print(response)
        response['_id'] = str(response['_id'])
        response['empleado'] = str(response['empleado'])
        return response

    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] = str(i['_id'])
            i['empleado'] = str(i['empleado'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        try:
            collection = self.db[self.collection]
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['empleado'] = str(response['empleado'])
            return response
        except:
            return {"status": False , "code": 400, "message": "no se encontro el id " + id}
