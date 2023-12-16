from models.producto import Producto
from repositories.repositorioProductos import RepositorioProductos


class ProductoController():
    def __init__(self):
        self.RepositorioProductos = RepositorioProductos()

    def create(self, infoProducto):
        try:
            infoProducto['disponible'] = True
            if infoProducto['nombre']!= None and infoProducto['referencia']!= None and infoProducto['imagenProducto']!= None and infoProducto['color']!= None and infoProducto['disponible'] != None:
                theProduct = Producto(infoProducto)
                print(theProduct)
                productoPorReferencia = self.RepositorioProductos.getByReferencia(theProduct.referencia)
                productoPorNombre = self.RepositorioProductos.getByNombre(theProduct.nombre)
                if not productoPorNombre and not productoPorReferencia:
                    response = self.RepositorioProductos.save(theProduct)
                    response.append({"status": True, "code": 200, "message": "El producto fue agregado a la base de datos con exito"})
                    return response
                else:
                    return {"status": False, "code": 400, "message": "ya existe un con la referencia dada o el mismo nombre de producto"}
        except:
            return {"status": False, "code": 400, "message": "el producto no pudo ser creado"}

    def getAllProducts(self):
        print("get all products")
        return self.RepositorioProductos.getAll()

    def getById(self,id):
        print("mostrando producto con : ", id)
        response =  self.RepositorioProductos.getById(id)
        if response != None:
            return response
        else:
            return {"status": False , "code": 400, "message": "No se encontro el producto con id: " + str(id)}

    def getByRef(self,referencia):
        print("mostrando prodcuto con referencia: "+ str(referencia))
        response = self.RepositorioProductos.getByReferencia(referencia)
        if response != None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No se encontro el producto con referencia: " + str(referencia)}


    def updateProduct(self, _id, infoProducto):
        print("actualizando un producto")
        dict = []
        if infoProducto["nombre"] and infoProducto["referencia"] and infoProducto["imagenProducto"] and infoProducto["cantidadTallaS"] and infoProducto["cantidadTallaM"] and infoProducto["cantidadTallaL"]:
            search = self.RepositorioProductos.getByReferencia(infoProducto["referencia"])
            print(search)
            if not search or str(search["_id"]) == _id:
                response = self.RepositorioProductos.update(_id, Producto(infoProducto))
                dict.append(response)
                dict.append({"status": True, "code": 200, "message": "el producto fue actualizado"})
                return response
            else:
                return {"status": False, "Code": 400, "message": "hace falta información o el id no fue encontrado"}

    def bloquearProducto(self,id):
        search = self.RepositorioProductos.getById(id)
        try:
            if search['disponible'] is True:
                productoUpdate = {
                    "nombre": search['nombre'],
                    "referencia": search['referencia'],
                    "imagenProducto": search['imagenProducto'],
                    "color": search['color'],
                    "disponible": False
                }
                print("xd")
                return self.RepositorioProductos.update(id,Producto(productoUpdate))
            else:
                return {"status":False, "code":400, "message": "el producto ya esta bloqueado"}
        except:
            return {"status": False, "code": 400, "message": "No se encontro el producto de id"+id}

    def desbloquearProducto(self,id):
        search = self.RepositorioProductos.getById(id)
        try:
            if search['disponible'] is False:
                productoUpdate = {
                    "nombre": search['nombre'],
                    "referencia": search['referencia'],
                    "imagenProducto": search['imagenProducto'],
                    "color": search['color'],
                    "disponible": True
                }
                return self.RepositorioProductos.update(id, Producto(productoUpdate))
            else:
                return {"status": False, "code": 400, "message": "el producto ya esta desbloqueado"}
        except:
            return {"status": False, "code": 400, "message": "No se encontro el producto de id" + id}

    def deleteProducto(self, _id):
        print("eliminar un producto")


        return self.RepositorioProductos.delete(_id)


