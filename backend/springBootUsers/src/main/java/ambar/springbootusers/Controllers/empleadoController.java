package ambar.springbootusers.Controllers;
import ambar.springbootusers.Modelos.empleado;
import ambar.springbootusers.Modelos.infoEmpleado;
import ambar.springbootusers.Modelos.rol;
import ambar.springbootusers.Modelos.userGeneral;
import ambar.springbootusers.Repositories.rolRepository;
import ambar.springbootusers.Repositories.empleadoRepository;
import ambar.springbootusers.Repositories.UserGeneralRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.SecurityProperties;
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
    @Autowired
    UserGeneralRepository myUserRepo;


    @PostMapping
    public empleado createEmpleado(@RequestBody infoEmpleado empleadoActual){

        userGeneral usuario = new userGeneral(empleadoActual.getIdEmpleado(),empleadoActual.getNombreApellido(),empleadoActual.getCorreo(),empleadoActual.getNumeroCelular(),empleadoActual.getPassword(),empleadoActual.getRol());
        empleado nuevoEmpleado = new empleado(empleadoActual.getIdEmpleado(),usuario, empleadoActual.getIdentificacion(),empleadoActual.getSede());
        if(nuevoEmpleado.getUsuario().isValid() && nuevoEmpleado.getIdentificacion() != null && nuevoEmpleado.getSede() != null){
            userGeneral usuarioGen = this.myUserRepo.getUserGeneralByCorreo(nuevoEmpleado.getUsuario().getCorreo());
            empleado searched = this.empleadoRepository.getempleadoByIdentificacion(nuevoEmpleado.getIdentificacion());
            if(searched == null && usuarioGen == null){
                nuevoEmpleado.getUsuario().setPassword(convertirSHA256(nuevoEmpleado.getUsuario().getPassword()));
                userGeneral response = this.myUserRepo.save(nuevoEmpleado.getUsuario());
                nuevoEmpleado.setUsuario(response);
                return this.empleadoRepository.save(nuevoEmpleado);
            }else{ throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "el empleado ya existe");
            }
        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Hace falta información para crear el empleado");
        }
    }

    @PostMapping("rol/{idRol}")
    public empleado createEmpleadowithRol(@RequestBody infoEmpleado empleadoActual, @PathVariable String idRol){
        userGeneral usuario = new userGeneral(empleadoActual.getIdEmpleado(),empleadoActual.getNombreApellido(),empleadoActual.getCorreo(),empleadoActual.getNumeroCelular(),empleadoActual.getPassword(),empleadoActual.getRol());
        empleado nuevoEmpleado = new empleado(empleadoActual.getIdEmpleado(),usuario, empleadoActual.getIdentificacion(),empleadoActual.getSede());
        if(nuevoEmpleado.getUsuario().isValid() && nuevoEmpleado.getIdentificacion() != null && nuevoEmpleado.getSede() != null){
            rol rolUsuario = this.rolRepo.findById(idRol).orElse(null);
            userGeneral usuarioGen = this.myUserRepo.getUserGeneralByCorreo(nuevoEmpleado.getUsuario().getCorreo());
            empleado searched = this.empleadoRepository.getempleadoByIdentificacion(nuevoEmpleado.getIdentificacion());
            if(searched == null && usuarioGen == null && rolUsuario != null){
                nuevoEmpleado.getUsuario().setRol(rolUsuario);
                nuevoEmpleado.getUsuario().setPassword(convertirSHA256(nuevoEmpleado.getUsuario().getPassword()));
                userGeneral response = this.myUserRepo.save(nuevoEmpleado.getUsuario());
                nuevoEmpleado.setUsuario(response);
                return this.empleadoRepository.save(nuevoEmpleado);
            }else{ throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "el empleado ya existe");
            }
        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Hace falta información para crear el empleado");
        }
    }

    @GetMapping
    public List<empleado> getAllEmpleado(){
        List<empleado> usuarios = this.empleadoRepository.findAll();
        return usuarios;
    }


    @GetMapping("{id}")
    public empleado getById(@PathVariable String id){
        empleado usuarioActual = this.empleadoRepository.findById(id).orElse(null);
        if(usuarioActual != null){
            return usuarioActual;
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontron ningun empleado con el id: " + id);
    }    @GetMapping("/getByUser/{idUser}")
    public empleado getEmpleadoByIdUser(@PathVariable String idUser){
        return this.empleadoRepository.getempleadoByUser(idUser);
    }


    @PutMapping("{id}")
    public empleado updateEmpleado(@PathVariable String id ,@RequestBody infoEmpleado informacionEmpleado){
        if(informacionEmpleado.getCorreo() != null && informacionEmpleado.getPassword()  != null && informacionEmpleado.getNumeroCelular() != null && informacionEmpleado.getSede() != null){
            empleado Validacion = this.empleadoRepository.findById(id).orElse(null);
            if (Validacion != null ){
                userGeneral usuario = this.myUserRepo.getUserGeneralByCorreo(informacionEmpleado.getCorreo());
                if (usuario == null || Validacion.getUsuario().get_id().equals(usuario.get_id())){
                    Validacion.getUsuario().setNombreApellido(informacionEmpleado.getNombreApellido());
                    Validacion.getUsuario().setPassword(convertirSHA256(informacionEmpleado.getPassword()));
                    Validacion.getUsuario().setCorreo(informacionEmpleado.getCorreo());
                    Validacion.getUsuario().setNumeroCelular(informacionEmpleado.getNumeroCelular());
                    Validacion.setIdentificacion(informacionEmpleado.getIdentificacion());
                    Validacion.setSede(informacionEmpleado.getSede());
                    this.myUserRepo.save(Validacion.getUsuario());
                    return this.empleadoRepository.save(Validacion);
                }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "ya existe un empleado con el correo: "+ informacionEmpleado.getCorreo());
            }else{
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontro ningun empleado con el id: " + id);
            }
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se tiene la información necesaria para actualizar al empleado");
    }

    @DeleteMapping("{id}")
    public empleado deleteUser(@PathVariable String id){
        empleado userToDelete = this.empleadoRepository.findById(id).orElse(null);

        if(userToDelete != null) {
            this.myUserRepo.deleteById(userToDelete.getUsuario().get_id());
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
