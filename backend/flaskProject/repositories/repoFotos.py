from repositories.interfaceRepositorio import interfaceRepositorio
from models.formatoFotos import formatoFotos
from bson import ObjectId

class RepoFotos(interfaceRepositorio[formatoFotos]):
    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find().sort("fecha",1)
        for i in response:
            i['_id'] =str(i['_id'])
            allItems.append(i)
        return allItems

    def getSinCompletar(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"estado": False}).sort("fecha",1)
        for i in response:
            i['_id'] =str(i['_id'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            return response
        else:
            return None
    pass

