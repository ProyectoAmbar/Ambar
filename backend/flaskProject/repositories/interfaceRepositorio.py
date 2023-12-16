import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json
T = TypeVar('T')
class interfaceRepositorio(Generic[T]):
    def __init__(self):
        ca = certifi.where()
        dataconfig = self.loadConfig()
        client = pymongo.MongoClient(dataconfig["data-db-connection"], tlsCAFile=ca)
        self.db = client[dataconfig["name-db"]]
        theClass = get_args(self.__orig_bases__[0])
        self.collection = theClass[0].__name__

    def loadConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data

    def save(self, item: T):
        dict = []
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        dict.append(response)
        return dict


    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
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

    def update(self,id , item:T):
        try:
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
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

    def query(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
        x = self.transformObjectIds(x)
        x = self.getValuesDBRef(x)

        return x
    def getDb(self):
        return self.db