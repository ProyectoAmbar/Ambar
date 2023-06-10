package ambar.springbootusers.Controllers;
import ambar.springbootusers.Repositories.rolRepository;
import ambar.springbootusers.Modelos.rol;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/rol")
public class rolController {
    @Autowired
    private rolRepository myRolRepository;

    @ResponseStatus(HttpStatus.ACCEPTED)
    @GetMapping("/getAll")
    public List<rol> getAll(){
        return this.myRolRepository.findAll();
    }

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public rol createRol(@RequestBody rol infoRol){
        infoRol.toString();
        rol search = this.myRolRepository.findTopByName(infoRol.getName());
        System.out.println(search);
        if(infoRol.isValid() && search == null){
            return this.myRolRepository.save(infoRol);
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El rol no cummle con los requisitos");
    }

}
