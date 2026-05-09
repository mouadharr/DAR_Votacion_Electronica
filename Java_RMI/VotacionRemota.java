import java.rmi.Remote;
import java.rmi.RemoteException;

public interface VotacionRemota extends Remote {
    // Para no andar mandando strings a mano por el socket
    String emitirVoto(String dni, String candidato) throws RemoteException;
    
    // Lo mismo que el "CERRAR" de antes
    String cerrarUrna() throws RemoteException;
}