package ambar.springbootusers.Modelos;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document
public class permiso {
    @Id
    String _id;
    String url;
    String metodo;


    public permiso(String _id, String url, String metodo) {
        this._id = _id;
        this.url = url;
        this.metodo = metodo;
    }

    public boolean isValid(){
        if(this.metodo != null && this.url != null){
            return true;
        }else{
            return false;
        }
    }
    public String get_id() {
        return _id;
    }

    public void set_id(String _id) {
        this._id = _id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getMetodo() {
        return metodo;
    }


    public void setMetodo(String metodo) {
        this.metodo = metodo;
    }
}
