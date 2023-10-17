from repositories.interfaceRepositorio import interfaceRepositorio
from models.caja import caja
class repoCaja(interfaceRepositorio[caja]):
    def getOne(self):
        collection = self.db[self.collection]
        response = collection.find()[0]
        response['_id'] = str(response['_id'])
        return response
    pass