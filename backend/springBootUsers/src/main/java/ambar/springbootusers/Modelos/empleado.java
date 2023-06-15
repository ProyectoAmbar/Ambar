package ambar.springbootusers.Modelos;
import ambar.springbootusers.Modelos.rol;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document
public class empleado extends userGeneral {
    private String identificacion;
    private String sede;


    public empleado(String _id, String nombreApellido, String correo, String numeroCelular, ambar.springbootusers.Modelos.rol rol, String identificacion, String sede) {
        super(_id, nombreApellido, correo, numeroCelular, rol);
        this.identificacion = identificacion;
        this.sede = sede;
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
