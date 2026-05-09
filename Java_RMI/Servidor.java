import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Servidor {
    public static void main(String[] args) {
        try {
            VotacionRemotaImpl servicioVotacion = new VotacionRemotaImpl();
            // Creamos el registro en el puerto de RMI por defecto
            Registry registry = LocateRegistry.createRegistry(1099); 
            registry.rebind("ServicioVotacion", servicioVotacion);
            
            System.out.println("Servidor activo. Esperando en el puerto 1099...");
        } catch (Exception e) {
            System.err.println("No se ha podido iniciar el servidor correctamente: " + e.getMessage());
        }
    }
}