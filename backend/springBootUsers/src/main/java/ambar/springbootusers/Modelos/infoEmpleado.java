package ambar.springbootusers.Modelos;

public class infoEmpleado {
    private String idEmpleado;
    private String idUser;
    private String nombreApellido;
    private String correo;
    private String password;
    private String identificacion;
    private String numeroCelular;
    private rol rol;

    public ambar.springbootusers.Modelos.rol getRol() {
        return rol;
    }

    public void setRol(ambar.springbootusers.Modelos.rol rol) {
        this.rol = rol;
    }

    public String getIdEmpleado() {
        return idEmpleado;
    }

    public void setIdEmpleado(String idEmpleado) {
        this.idEmpleado = idEmpleado;
    }

    public String getNumeroCelular() {
        return numeroCelular;
    }

    public void setNumeroCelular(String numeroCelular) {
        this.numeroCelular = numeroCelular;
    }

    public String getIdUser() {
        return idUser;
    }

    public void setIdUser(String idUser) {
        this.idUser = idUser;
    }



    private String sede;

    public infoEmpleado(String idEmpleado, String idUser, String nombreApellido, String correo, String password, String numeroCelular, String identificacion, String sede, rol rol) {
        this.idEmpleado = idEmpleado;
        this.idUser = idUser;
        this.nombreApellido = nombreApellido;
        this.correo = correo;
        this.password = password;
        this.numeroCelular = numeroCelular;
        this.rol = rol;
        this.identificacion = identificacion;
        this.sede = sede;
    }

    public String getNombreApellido() {
        return nombreApellido;
    }

    public void setNombreApellido(String nombreApellido) {
        this.nombreApellido = nombreApellido;
    }

    public String getCorreo() {
        return correo;
    }

    public void setCorreo(String correo) {
        this.correo = correo;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
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
