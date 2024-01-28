from repositories.interfaceRepositorio import interfaceRepositorio
from models.tareaModisteria import tareaModisteria
from bson import ObjectId,DBRef
from datetime import date

class repoTareaModista(interfaceRepositorio[tareaModisteria]):
    def save(self, item: tareaModisteria):
        print("def save")
        print(item.modista)
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['formMedidas'] = str(response['formMedidas'])
        response['producto'] = str(response['producto'])
        response['formulario'] = str(response['formulario'])

        if response['modista'] is not None:
            response['modista'] = str(response['modista'])
        else:
            response['modista'] = None
        return response


    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['formMedidas'] = str(i['formMedidas'])
            i['modista'] = str(i['modista'])
            i['producto'] = str(i['producto'])
            i['formulario'] = str(i['formulario'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        try:
            if response != None:
                response['_id'] = str(response['_id'])
                response['formMedidas'] = str(response['formMedidas'])
                response['modista'] = str(response['modista'])
                response['producto'] = str(response['producto'])
                response['formulario'] = str(response['formulario'])
            return response
        except:
            return {"status": False, "code": 400, "message": "no se encontro la tarea de modisteria"}

    def getCompletedTask(self,id):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"$and": [{"modista": DBRef("empleado", ObjectId(id))}, {"completado": True}]})
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formMedidas'] = str(item['formMedidas'])
                item['modista'] = str(item['modista'])
                item['producto'] = str(item['producto'])
                item['formulario'] = str(item['formulario'])
                allItems.append(item)
        return allItems






    def getByFormulario(self,formulario):
        collection = self.db[self.collection]
        response = collection.find_one({'formulario': DBRef('formatoAlquiler', ObjectId(formulario))})
        try:
            if response != None:
                response['_id'] = str(response['_id'])
                response['formMedidas'] = str(response['formMedidas'])
                response['modista'] = str(response['modista'])
                response['producto'] = str(response['producto'])
                response['formulario'] = str(response['formulario'])
            return response
        except:
            return {"status": False, "code": 400, "message": "no se encontro la tarea de modisteria"}

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        return response
    def update(self,id , item:tareaModisteria):
        try:
            dict = []
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['formMedidas'] = str(response['formMedidas'])
            response['modista'] = str(response['modista'])
            response['producto'] = str(response['producto'])
            response['formulario'] = str(response['formulario'])
            dict.append(response)
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

    def getTareasPendientes(self,idModista):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"completado": False}, {"fecha": {"$gte": str(date.today())}},{"modista": DBRef('empleado', ObjectId(idModista))}]}
        response = collection.find(query).sort("fecha",1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formMedidas'] = str(item['formMedidas'])
                item['modista'] = str(item['modista'])
                item['producto'] = str(item['producto'])
                item['formulario'] = str(item['formulario'])
                allItems.append(item)
        return allItems

    def getAllTareasPendientes(self):
        allItems = []
        collection = self.db[self.collection]
        query = {"completado": False}
        response = collection.find(query).sort("fecha",1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formMedidas'] = str(item['formMedidas'])
                item['modista'] = str(item['modista'])
                item['producto'] = str(item['producto'])
                item['formulario'] = str(item['formulario'])
                allItems.append(item)
        return allItems

    def getByFormulario(self,formulario):
        collection = self.db[self.collection]
        response = collection.find_one({'formulario':  DBRef('formatoAlquiler', ObjectId(formulario))})
        try:
            if response != None:
                response['_id'] = str(response['_id'])
                response['formMedidas'] = str(response['formMedidas'])
                response['modista'] = str(response['modista'])
                response['producto'] = str(response['producto'])
                response['formulario'] = str(response['formulario'])
            return response
        except:
            return {"status": False, "code": 400, "message": "no se encontro la tarea de modisteria"}

    def getTareasSinAsignar(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"modista":None})
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formMedidas'] = str(item['formMedidas'])
                item['producto'] = str(item['producto'])
                item['formulario'] = str(item['formulario'])
                allItems.append(item)
        return allItems

    pass