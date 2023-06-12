package ambar.springbootusers.Controllers;
import ambar.springbootusers.Repositories.rolRepository;
import ambar.springbootusers.Modelos.rol;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import javax.management.Query;
import java.net.HttpRetryException;
import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/rol")
public class rolController {
    @Autowired
    private rolRepository myRolRepository;

    //obtener todos los roles
    @ResponseStatus(HttpStatus.ACCEPTED)
    @GetMapping
    public List<rol> getAll(){
        return this.myRolRepository.findAll();
    }

    //crear un rol
    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public rol createRol(@RequestBody rol infoRol){
        infoRol.toString();
        rol search = this.myRolRepository.findTopByName(infoRol.getName());
        if(infoRol.isValid() && search == null){
            return this.myRolRepository.save(infoRol);
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El rol no cumple con los requisitos");
    }

    //obtener un usuario por su id
    @ResponseStatus(HttpStatus.ACCEPTED)
    @GetMapping("{id}")
    public rol getRolById(@PathVariable String id){
        rol searched = this.myRolRepository.findById(id).orElse(null);
        if(searched == null){
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"El id" + id +" no fue encontrado" );
        }
        return searched;
    }
    // editar un rol
    @ResponseStatus(HttpStatus.ACCEPTED)
    @PutMapping("{id}")
    public rol updateRol(@PathVariable String id,@RequestBody rol updateRol){
        rol rolActual = this.myRolRepository.findById(id).orElse(null);
        if(rolActual != null){
            rolActual.setName(updateRol.getName());
            rolActual.setName(updateRol.getDescription());
            return this.myRolRepository.save(rolActual);
        }else {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        }
    }

    @ResponseStatus(HttpStatus.ACCEPTED)
    @DeleteMapping("{id}")
    public rol deleteRol(@PathVariable String id){
        rol rolAEliminar = this.myRolRepository.findById(id).orElse(null);
        if(rolAEliminar != null){
            this.myRolRepository.delete(rolAEliminar);
            throw new ResponseStatusException(HttpStatus.ACCEPTED,"se ha eliminado el rol con id " + id);
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"el rol de id " + id +" no existe");
    }

}
