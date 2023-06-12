package ambar.springbootusers.Controllers;
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

    @PostMapping
    public userGeneral createUser(@RequestBody userGeneral usuario){
        if(usuario.isValid()){
            userGeneral usuarioActual = this.myUserRepo.getUerGeneralByCorreo(usuario.getCorreo());
            if(usuarioActual == null){
                usuario.setPassword(convertirSHA256(usuario.getPassword()));
                rol defaultRol = this.myRolRepo.findById("64869b530152eb1976abcee4").orElse(null);
                usuario.setRol(defaultRol);
                return this.myUserRepo.save(usuario);
            }else{
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Ya existe un usuario con el correo: " + usuario.getCorreo() );
            }

        }else{
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "al usuario le hace falta información");
        }
    }

    @GetMapping
    public List<userGeneral> getAllUser(){
        List<userGeneral> usuarios = this.myUserRepo.findAll();
        if(usuarios != null){
            return usuarios;
        }
        throw new ResponseStatusException(HttpStatus.OK);
    }

    @GetMapping("{id}")
    public userGeneral getById(@PathVariable String id){
        userGeneral usuarioActual = this.myUserRepo.findById(id).orElse(null);
        if(usuarioActual != null){
            return usuarioActual;
        }else throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No se encontron ningun usuario con el id: " + id);
    }

    @PostMapping("/validar")
    public userGeneral validar(@RequestBody userGeneral usuarioValidar) {
        userGeneral usuarioActual = this.myUserRepo.getUerGeneralByCorreo(usuarioValidar.getCorreo());
        if(usuarioActual != null && usuarioActual.getPassword().equals(convertirSHA256(usuarioValidar.getPassword()))) {
            throw new ResponseStatusException(HttpStatus.ACCEPTED);
        }else throw new ResponseStatusException(HttpStatus.UNAUTHORIZED);

    }

    @PutMapping("{id}")
    public userGeneral updateUser(@PathVariable String id ,@RequestBody userGeneral usuario){
        if(usuario.isValid()){
            userGeneral Validacion = this.myUserRepo.getUerGeneralByCorreo(usuario.getCorreo());
            if (Validacion == null || Validacion.get_id() == id){
                Validacion = usuario;
                return Validacion;
            }else{
                throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "el correo ya tiene un usuario asignado");
            }
        }
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "no se tiene la información necesaria para actualizar al usuario");
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
