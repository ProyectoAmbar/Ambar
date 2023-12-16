package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.empleado;
import ambar.springbootusers.Modelos.userGeneral;
import org.springframework.data.mongodb.core.mapping.DBRef;
import  org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;


public interface empleadoRepository extends MongoRepository<empleado,String>{

    @Query("{'correo': ?0}")
    public userGeneral getempleadoByCorreo(String correo);
    @Query(" {'identificacion': ?0}")
    public empleado getempleadoByIdentificacion(String identificacion);

    @Query("{'usuario':  ?0}")
    public empleado getempleadoByUser(String usuarioId);


}
