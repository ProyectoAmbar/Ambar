package ambar.springbootusers.Controllers;
import ambar.springbootusers.Modelos.empleado;
import ambar.springbootusers.Modelos.userGeneral;
import ambar.springbootusers.Modelos.rol;
import ambar.springbootusers.Repositories.rolRepository;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import ambar.springbootusers.Repositories.UserGeneralRepository;
import org.springframework.web.server.ResponseStatusException;

import javax.sound.midi.MidiUnavailableException;
import java.io.IOException;
import java.util.List;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

@Data
@RestController
@RequestMapping("/user")
public class userController {
    @Autowired
    private UserGeneralRepository myUserRepo;
    @Autowired
    private rolRepository myRolRepo;


    //CREAR UN NUEVO USUARIO
    @PostMapping
    public userGeneral createUser(@RequestBody userGeneral usuario){
        if(usuario.isValid()){
            userGeneral usuarioActual = this.myUserRepo.getUserGeneralByCorreo(usuario.getCorreo());
            if(usuarioActual == null){
                usuario.setPassword(convertirSHA256(usuario.getPassword()));
                rol defaultRol = this.myRolRepo.findById("64ada40b4858ec4ec0aecf7b").orElse(null);
                usuario.setRol(defaultRol);
                return this.myUserRepo.save(usuario);
            }else{
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Ya existe un usuario con el correo: " + usuario.getCorreo() );
            }

        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "al usuario le hace falta información");
        }
    }
    @PostMapping("/rol/{idRol}")
    public userGeneral createUderwWithRol(@RequestBody userGeneral usuario, @PathVariable String idRol){
        if(usuario.isValid()){
            userGeneral usuarioActual = this.myUserRepo.getUserGeneralByCorreo(usuario.getCorreo());
            if(usuarioActual == null){
                usuario.setPassword(convertirSHA256(usuario.getPassword()));
                rol Rol = this.myRolRepo.findById(idRol).orElse(null);
                if(Rol != null){
                    usuario.setRol(Rol);
                }
                return this.myUserRepo.save(usuario);
            }else{
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Ya existe un usuario con el correo: " + usuario.getCorreo() );
            }

        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "al usuario le hace falta información");
        }
    }


    //OBTENER TODOS LOS USUARIOS
    @GetMapping
    public List<userGeneral> getAllUser(){
        List<userGeneral> usuarios = this.myUserRepo.findAll();
        if(usuarios != null){
            return usuarios;
        }
        throw new ResponseStatusException(HttpStatus.OK);
    }


    //OBTENER UN USUARIO POR SU ID
    @GetMapping("{id}")
    public userGeneral getById(@PathVariable String id){
        userGeneral usuarioActual = this.myUserRepo.findById(id).orElse(null);
        if(usuarioActual != null){
            return usuarioActual;
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontron ningun usuario con el id: " + id);
    }


    //VALIDAR LAS CREDENCIALES DE UN USUARIO
    @PostMapping("/validar")
    public userGeneral validar(@RequestBody userGeneral usuarioValidar) {
        userGeneral usuarioActual = this.myUserRepo.getUserGeneralByCorreo(usuarioValidar.getCorreo());
        System.out.println(usuarioActual);
        if(usuarioActual != null && usuarioActual.getPassword().equals(convertirSHA256(usuarioValidar.getPassword()))) {
            return  usuarioActual;
        }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED);
    }


    //  ACTUALIZAR USUARIO
    @PutMapping("{id}")
    public userGeneral updateUser(@PathVariable String id ,@RequestBody userGeneral usuario){
        if(usuario.isValid()){
            userGeneral Validacion = this.myUserRepo.findById(id).orElse(null);
            if (Validacion != null ){
                userGeneral validarCorreo = this.myUserRepo.getUserGeneralByCorreo(usuario.getCorreo());
                if (validarCorreo == null || validarCorreo.get_id() == id){
                    Validacion.setNombreApellido(usuario.getNombreApellido());
                    Validacion.setPassword(convertirSHA256(usuario.getPassword()));
                    Validacion.setCorreo(usuario.getCorreo());
                    Validacion.setNumeroCelular(usuario.getNumeroCelular());
                    return this.myUserRepo.save(Validacion);
                }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "ya existe un usuario con el correo: "+ usuario.getCorreo());
            }else{
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontro ningun usuario con el id: " + id);
            }
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se tiene la información necesaria para actualizar al usuario");
    }
    //ASIGNAR ROL
    @PutMapping("/asignarRol/{idUsuario}/rol/{idRol}")
    public userGeneral asignarRol(@PathVariable String idUsuario, @PathVariable String idRol){
        rol rolAAsignar = this.myRolRepo.findById(idRol).orElse(null);
        userGeneral usuarioActual = this.myUserRepo.findById(idUsuario).orElse(null);
        if(rolAAsignar != null && usuarioActual != null){
            usuarioActual.setRol(rolAAsignar);
            return this.myUserRepo.save(usuarioActual);
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No ha sido posible encontrar el usuario o el Id");
    }
    // ELIMINAR UN USUARIO
    @DeleteMapping("{id}")
    public userGeneral deleteUser(@PathVariable String id){
        userGeneral userToDelete = this.myUserRepo.findById(id).orElse(null);
        if(userToDelete != null) {
            this.myUserRepo.deleteById(id);
            return userToDelete;
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No existe ningun usuario con el id :" + id );
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
