package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.PermisosRol;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface permisosRolRepository extends MongoRepository<PermisosRol, String>{
}
