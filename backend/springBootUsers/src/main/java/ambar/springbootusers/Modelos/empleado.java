package ambar.springbootusers.Modelos;
import ambar.springbootusers.Modelos.rol;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;


@Document
public class empleado {
    @Id
    private String id;
    private String identificacion;
    private String sede;
    @DBRef
    private userGeneral usuario;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public userGeneral getUsuario() {
        return usuario;
    }

    public void setUsuario(userGeneral usuario) {
        this.usuario = usuario;
    }

    public empleado(String id, userGeneral usuario, String identificacion, String sede){
        this.id = id;
        this.usuario = usuario;
        this.identificacion = identificacion;
        this.sede = sede;
    }


    public empleado(){
        this.id = null;
        this.usuario = null;
        this.identificacion = null;
        this.sede = null;
    }


    public String getIdentificacion() {
        return identificacion;
    }

    public void setIdentificacion(String identificacion) {
        this.identificacion = identificacion;
    }

    public String getSede() {
        return sede;
    }

    public void setSede(String sede) {
        this.sede = sede;
    }
}
