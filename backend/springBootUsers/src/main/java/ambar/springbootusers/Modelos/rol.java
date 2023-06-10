package ambar.springbootusers.Modelos;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;




@Data
@Document
public class rol {
    @Id
    private String _id;
    private String name;
    private String description;
    public String get_id() {
        return _id;
    }

    public String toString(){
        System.out.println(this.name);
        System.out.println(this.description);
        return null;
    }


    public boolean isValid(){
        if (this.name == null || this.description == null){
            return false;
        }
        return true;
    }
    public void set_id(String _id) {
        this._id = _id;
    }

    public String getNombre() {
        return name;
    }

    public void setNombre(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }


}
