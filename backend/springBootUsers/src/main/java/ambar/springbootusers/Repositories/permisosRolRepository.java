package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.PermisosRol;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import java.util.List;


public interface permisosRolRepository extends MongoRepository<PermisosRol, String>{
    @Query("{'rol':?0}")
    public List<PermisosRol> getAllByRol(String rolId);
    @Query("{$and : [{'rol': {$eq :?0}},{'permiso': {$eq: ?1}}]}")
    public PermisosRol getPermisosRolByPermisoAndRol(String idPermiso, String idRol);
}
