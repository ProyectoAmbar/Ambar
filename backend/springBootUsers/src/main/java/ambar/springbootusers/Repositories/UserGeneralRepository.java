package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.userGeneral;
import  org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface UserGeneralRepository extends MongoRepository<userGeneral,String>{
    @Query("{correo: ?0}")
    public userGeneral getUserGeneralByCorreo(String correo);
}
