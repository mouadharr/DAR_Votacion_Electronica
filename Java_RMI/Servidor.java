import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Servidor {
    public static void main(String[] args) {
        try {
            VotacionRemotaImpl servicioVotacion = new VotacionRemotaImpl();
            // Registro RMI en el puerto 1099 
            Registry registry = LocateRegistry.createRegistry(1099); 
            registry.rebind("ServicioVotacion", servicioVotacion);
            
            System.out.println("Servidor listo en el 1099...");
        } catch (Exception e) {
            System.err.println("Error al arrancar el server: " + e.getMessage());
        }
    }
}
