package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.empleado;
import  org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface empleadoRepository extends MongoRepository<empleado,String>{

    @Query("{'correo': ?0}")
    public empleado getempleadoByCorreo(String correo);
    @Query(" {$and:  [{'correo':  ?0},{'indentificacion': ?1}]}")
    public empleado getempleadoByCorreoIdentificacion(String correo, String identificacion);
}
