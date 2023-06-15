package ambar.springbootusers.Controllers;
import ambar.springbootusers.Modelos.permiso;
import ambar.springbootusers.Repositories.permisosRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("permisos")
public class permisosController {
    @Autowired
    permisosRepository permisosRepo;

    @PostMapping
    public permiso crearPermiso(@RequestBody permiso permisoACrear){
        if(permisoACrear.isValid()){
            permiso searched = this.permisosRepo.getpermisoByUrlAndMetodo(permisoACrear.getUrl(),permisoACrear.getMetodo());
            if(searched == null){
                return this.permisosRepo.save(permisoACrear);
            }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Ya existe ese permiso");
        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Hace falta información para crear el permiso");
        }
    }

    @GetMapping
    public List<permiso> getAllPermisos(){
        return this.permisosRepo.findAll();
    }
    @GetMapping("{id}")
    public permiso getPermisoById(@PathVariable String id){
        permiso search = this.permisosRepo.findById(id).orElse(null);
        if(search != null){
            return search;
        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se ha encontrado un permiso con el id" + id);
        }
    }

    
}
