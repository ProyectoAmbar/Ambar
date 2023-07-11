package ambar.springbootusers.Controllers;
import ambar.springbootusers.Modelos.PermisosRol;
import ambar.springbootusers.Modelos.rol;
import ambar.springbootusers.Modelos.permiso;
import ambar.springbootusers.Repositories.permisosRolRepository;
import ambar.springbootusers.Repositories.permisosRepository;
import ambar.springbootusers.Repositories.rolRepository;


import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@CrossOrigin
@RestController
@RequestMapping("PermisosRol")
public class permisosRolController {

    @Autowired
    private rolRepository myRolRepository;
    @Autowired
    private permisosRolRepository myPermisosRolRepo;
    @Autowired
    private permisosRepository myPermisosRepo;
    @GetMapping
    public List<PermisosRol> getAllPermisosRol(){
        return this.myPermisosRolRepo.findAll();
    }

    @GetMapping("{id}")
    public PermisosRol getPermisoById(@PathVariable String id){
        PermisosRol search = this.myPermisosRolRepo.findById(id).orElse(null);
        if(search != null){
            return search;
        }else {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se encontro el Permisos Rol con el id" + id);
        }
    }

    @PostMapping("/permiso/{idPermiso}/rol/{idRol}")
    public PermisosRol createPermisosRol(@PathVariable String idPermiso, @PathVariable String idRol){
        PermisosRol validacion = this.myPermisosRolRepo.getPermisosRolByPermisoAndRol(idPermiso,idRol);
        if(validacion == null){
            rol rolAsignar = this.myRolRepository.findById(idRol).orElse(null);
            System.out.println(rolAsignar);
            permiso permisoAsignar = this.myPermisosRepo.findById(idPermiso).orElse(null);
            System.out.println(permisoAsignar);
            if(rolAsignar != null && permisoAsignar != null){
                PermisosRol nuevoPermisoRol = new PermisosRol();
                nuevoPermisoRol.setRol(rolAsignar);
                nuevoPermisoRol.setPermiso(permisoAsignar);
                return this.myPermisosRolRepo.save(nuevoPermisoRol);
            }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontro el permiso o el rol a asignar");
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "ya existe un PermisoRol con los mismos atributos");
    }

    @GetMapping("/validar-permiso/rol/{id}")
    public PermisosRol validate(@PathVariable String id,@RequestBody  permiso permiso, final HttpServletResponse response )throws IOException{
        List<PermisosRol> permisosRoles = this.myPermisosRolRepo.getAllByRol(id);

        System.out.println(permiso);

        PermisosRol tienePermiso= null;

        for( int i=0;i<permisosRoles.size();i++){
            System.out.println();
            if(permisosRoles.get(i) != null && permisosRoles.get(i) != null){
                if(permisosRoles.get(i).getPermiso().getMetodo().equals(permiso.getMetodo()) & permisosRoles.get(i).getPermiso().getUrl().equals(permiso.getUrl())){

                    tienePermiso=permisosRoles.get(i);

                    break;
                }
            }

        }

        System.out.println(permisosRoles);

        System.out.println(tienePermiso);
        return tienePermiso;
    }



    @PutMapping("{Id}/permiso/{idPermiso}/rol/{idRol}")
    public PermisosRol updatePermisoRol(@PathVariable String Id, @PathVariable String idRol, @PathVariable String idPermiso){
        PermisosRol search = this.myPermisosRolRepo.findById(Id).orElse(null);
        rol rolupdate = this.myRolRepository.findById(idRol).orElse(null);
        permiso permisoUpdate = this.myPermisosRepo.findById(idPermiso).orElse(null);
        if(search != null && rolupdate != null && permisoUpdate != null){
            search.setRol(rolupdate);
            search.setPermiso(permisoUpdate);
            return this.myPermisosRolRepo.save(search);
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Hace falta información para actualizar el permisoRol");
    }

    @DeleteMapping("{id}")
    public permisosRolRepository deletePermisosRoles(@PathVariable String id) throws ResponseStatusException {
        PermisosRol search = this.myPermisosRolRepo.findById(id).orElse(null);
        if(search != null){
            this.myPermisosRolRepo.deleteById(id);
            throw new ResponseStatusException(HttpStatus.OK, "PermisoRol a sido eliminado");
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se ha encontrado el permisoRol con id");
    }

}
