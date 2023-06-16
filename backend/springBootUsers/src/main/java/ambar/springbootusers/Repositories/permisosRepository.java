package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.permiso;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface permisosRepository extends MongoRepository<permiso,String>{
    @Query("{$and: [{'url': ?0},{'metodo': ?1}] }")
    public permiso getpermisoByUrlAndMetodo(String url, String metodo);

}
