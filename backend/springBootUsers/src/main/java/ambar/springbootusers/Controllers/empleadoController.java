package ambar.springbootusers.Controllers;
import ambar.springbootusers.Modelos.empleado;
import ambar.springbootusers.Modelos.userGeneral;
import ambar.springbootusers.Repositories.rolRepository;
import ambar.springbootusers.Repositories.empleadoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("empleado")
public class empleadoController{
    @Autowired
    rolRepository rolRepo;
    @Autowired
    empleadoRepository empleadoRepository;

    @PostMapping
    public empleado createEmpleado(@RequestBody empleado empleadoActual){

        if(empleadoActual.isValid() && empleadoActual.getIdentificacion() != null && empleadoActual.getSede() != null){
            empleado searched = this.empleadoRepository.getempleadoByCorreoIdentificacion(empleadoActual.getCorreo(),empleadoActual.getIdentificacion());
            if(searched == null){
                empleadoActual.setPassword(convertirSHA256(empleadoActual.getPassword()));
                return this.empleadoRepository.save(empleadoActual);
            }else{ throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "el empleado ya existe");
            }
        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Hace falta información para crear el empleado");
        }
    }

    @GetMapping
    public List<empleado> getAllEmpleado(){
        List<empleado> usuarios = this.empleadoRepository.findAll();
        if(usuarios != null){
            return usuarios;
        }
        throw new ResponseStatusException(HttpStatus.OK);
    }

    @GetMapping("{id}")
    public empleado getById(@PathVariable String id){
        empleado usuarioActual = this.empleadoRepository.findById(id).orElse(null);
        if(usuarioActual != null){
            return usuarioActual;
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontron ningun empleado con el id: " + id);
    }

    @PutMapping("{id}")
    public empleado updateUser(@PathVariable String id ,@RequestBody empleado usuario){
        if(usuario.isValid()){
            empleado Validacion = this.empleadoRepository.findById(id).orElse(null);
            if (Validacion != null ){
                empleado validarCorreo = this.empleadoRepository.getempleadoByCorreo(usuario.getCorreo());
                if (validarCorreo == null || validarCorreo.get_id() == id){
                    Validacion.setNombreApellido(usuario.getNombreApellido());
                    Validacion.setPassword(convertirSHA256(usuario.getPassword()));
                    Validacion.setCorreo(usuario.getCorreo());
                    Validacion.setNumeroCelular(usuario.getNumeroCelular());
                    Validacion.setSede(usuario.getSede());
                    return this.empleadoRepository.save(Validacion);
                }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "ya existe un empleado con el correo: "+ usuario.getCorreo());
            }else{
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontro ningun empleado con el id: " + id);
            }
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se tiene la información necesaria para actualizar al empleado");
    }

    //VALIDAR LAS CREDENCIALES DE UN USUARIO
    @PostMapping("/validar")
    public empleado validar(@RequestBody empleado usuarioValidar) {
        empleado usuarioActual = this.empleadoRepository.getempleadoByCorreo(usuarioValidar.getCorreo());
        if(usuarioActual != null && usuarioActual.getPassword().equals(convertirSHA256(usuarioValidar.getPassword()))) {
            return  usuarioActual;
        }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED);
    }

    @DeleteMapping("{id}")
    public empleado deleteUser(@PathVariable String id){
        empleado userToDelete = this.empleadoRepository.findById(id).orElse(null);
        System.out.println(userToDelete.getCorreo());
        if(userToDelete != null) {
            this.empleadoRepository.deleteById(id);
            return userToDelete;
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No existe ningun empleado con el id :" + id );
    }

    public String convertirSHA256(String password) {
        MessageDigest md = null;
        try {
            md = MessageDigest.getInstance("SHA-256");
        }
        catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
        byte[] hash = md.digest(password.getBytes());
        StringBuffer sb = new StringBuffer();
        for(byte b : hash) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }


}
