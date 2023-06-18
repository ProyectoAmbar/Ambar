package ambar.springbootusers.Modelos;
import ambar.springbootusers.Modelos.permiso;
import ambar.springbootusers.Modelos.rol;

import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.DBRef;

@Data
@Document
public class PermisosRol {
    @Id
    private String _id;
    @DBRef
    private rol rol;
    @DBRef
    private permiso permiso;

    public PermisosRol(String _id, rol rol, permiso permiso){
        this._id = _id;
        this.rol = rol;
        this.permiso = permiso;
    }

    public PermisosRol (){}


    public String get_id() {
        return _id;
    }

    public void set_id(String _id) {
        this._id = _id;
    }

    public ambar.springbootusers.Modelos.rol getRol() {
        return rol;
    }

    public void setRol(ambar.springbootusers.Modelos.rol rol) {
        this.rol = rol;
    }

    public ambar.springbootusers.Modelos.permiso getPermiso() {
        return permiso;
    }

    public void setPermiso(ambar.springbootusers.Modelos.permiso permiso) {
        this.permiso = permiso;
    }
}
