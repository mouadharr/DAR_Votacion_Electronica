import java.rmi.Remote;
import java.rmi.RemoteException;

public interface VotacionRemota extends Remote {
    // Sustituye a mandar el texto "VOTAR dni candidato" por el socket
    String emitirVoto(String dni, String candidato) throws RemoteException;
    
    // Sustituye a mandar "CERRAR"
    String cerrarUrna() throws RemoteException;
}