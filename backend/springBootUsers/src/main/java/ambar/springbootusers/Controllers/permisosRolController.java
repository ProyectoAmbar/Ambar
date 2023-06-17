package ambar.springbootusers.Controllers;
import ambar.springbootusers.Modelos.PermisosRol;
import ambar.springbootusers.Modelos.rol;
import ambar.springbootusers.Modelos.permiso;
import ambar.springbootusers.Repositories.permisosRolRepository;
import ambar.springbootusers.Repositories.permisosRepository;
import ambar.springbootusers.Repositories.rolRepository;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpRange;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@CrossOrigin
@RestController
@RequestMapping("PermisosrRol")
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

    @GetMapping("[id")
    public PermisosRol getPermisoById(@PathVariable String _id){
        PermisosRol search = this.myPermisosRolRepo.findById(_id).orElse(null);
        if(search != null){
            return search;
        }else {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se encontro el Permisos Rol con el id" + _id);
        }
    }

    @PostMapping
    public PermisosRol createPermisosRol(@RequestBody PermisosRol permisosRolInfo){
        if (permisosRolInfo.getRol() != null && permisosRolInfo.getPermiso()!= null){
            return this.myPermisosRolRepo.save(permisosRolInfo);
        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se posee la infomración necesaria");
        }
    }

    @GetMapping("/validar-permiso/rol/{id}")
    public PermisosRol validate(@PathVariable String id,@RequestBody  permiso permiso){


        List<PermisosRol> permisosRoles = this.myPermisosRolRepo.getAllByRol(id);

        System.out.println(permiso);

        PermisosRol tienePermiso= null;

        for( int i=0;i<permisosRoles.size();i++){
            if(permisosRoles.get(i).getPermiso().getMetodo().equals(permiso.getMetodo()) & permisosRoles.get(i).getPermiso().getUrl().equals(permiso.getUrl())){

                tienePermiso=permisosRoles.get(i);

                break;
            }
        }

        System.out.println(permisosRoles);

        System.out.println(tienePermiso);
        return tienePermiso;
    }


    @PutMapping("{Id}/rolID/{idRol}/permisoId/{idPermiso}")
    public PermisosRol updatePermisoRol(@PathVariable String _id, @PathVariable String idRol, @PathVariable String idPermiso){
        PermisosRol search = this.myPermisosRolRepo.findById(_id).orElse(null);
        rol rolupdate = this.myRolRepository.findById(idRol).orElse(null);
        permiso permisoUpdate = this.myPermisosRepo.findById(idPermiso).orElse(null);
        if(search != null && rolupdate != null && permisoUpdate != null){
            search.setRol(rolupdate);
            search.setPermiso(permisoUpdate);
            return this.myPermisosRolRepo.save(search);
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Hace falta información para actualizar el permisoRol");
    }

    @DeleteMapping("{id}")
    public permisosRolRepository deletePermisosRoles(@PathVariable String _id){
        PermisosRol search = this.myPermisosRolRepo.findById(_id).orElse(null);
        if(search != null){
            this.myPermisosRolRepo.deleteById(_id);
            throw new ResponseStatusException(HttpStatus.OK, "el usuario a sido eliminado");
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se ha encontrado el permisoRol con id");
    }

}
