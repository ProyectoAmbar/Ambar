from repositories.interfaceRepositorio import interfaceRepositorio
from models.FormatoAlquiler import formatoAlquiler
from bson.objectid import ObjectId


class repositorioFormatoAlquiler(interfaceRepositorio[formatoAlquiler]):
    def save(self, formAlquiler):
        dict = []
        print("def save")
        collection = self.db['formatoAlquiler']
        inserted = collection.insert_one(formAlquiler.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        print(response)
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        response['Producto'] = str(response['Producto'])
        response['Cliente'] = str(response['Cliente'])
        dict.append(response)
        return dict
    pass