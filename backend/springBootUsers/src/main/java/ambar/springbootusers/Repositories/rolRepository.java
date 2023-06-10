package ambar.springbootusers.Repositories;
import ambar.springbootusers.Modelos.rol;
import org.springframework.data.mongodb.repository.ExistsQuery;
import  org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface rolRepository extends MongoRepository<rol,String>{
    @Query("{'name': ?0}")
    public rol findTopByName(String name);
}
