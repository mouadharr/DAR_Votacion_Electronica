import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Collections;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

public class VotacionRemotaImpl extends UnicastRemoteObject implements VotacionRemota {
    
    // Usamos Map y Set concurrentes para que los hilos no se pisen
    private Map<String, Integer> opcionesVoto;
    private Set<String> censoVotantes;
    // volatile para que el cambio de estado de la urna se propague al momento
    private volatile boolean urnaAbierta; 

    public VotacionRemotaImpl() throws RemoteException {
        super();
        this.opcionesVoto = new ConcurrentHashMap<>();
        this.opcionesVoto.put("andrea_martos", 0);
        this.opcionesVoto.put("javier_garcia", 0);
        this.opcionesVoto.put("pedro_gomez", 0);
        
        // Censo de votantes, sincronizado para evitar lios
        this.censoVotantes = Collections.synchronizedSet(new HashSet<>());
        this.urnaAbierta = true;
    }

    @Override
    public String emitirVoto(String dni, String candidato) throws RemoteException {
        // Valido el DNI igual que en Python (9 char, 8 numeros y una letra)
        if (dni == null || dni.length() != 9 || !dni.substring(0, 8).matches("\\d+") || !Character.isLetter(dni.charAt(8))) {
            return "dni_invalido";
        }
        
        String opcion = candidato.toLowerCase();
        if (!opcionesVoto.containsKey(opcion)) {
            return "candidato_inexistente";
        }
        
        if (!urnaAbierta) {
            return "urna_cerrada";
        }

        // Si se mete bien en el set es que no había votado. Si devuelve false, ya votó.
        if (!censoVotantes.add(dni)) {
            return "dni_ya_registrado";
        }
        
        // Sumo un voto
        opcionesVoto.put(opcion, opcionesVoto.get(opcion) + 1);
        System.out.println("Voto de " + dni + " para " + opcion + " registrado correctamente");
        return "voto_confirmado";
    }

    @Override
    // synchronized en el cierre para que nadie vote mientras calculamos los ganadores
    public synchronized String cerrarUrna() throws RemoteException {
        if (!urnaAbierta) {
            return "urna_ya_cerrada_previamente";
        }
        
        urnaAbierta = false;
        int totalVotos = opcionesVoto.values().stream().mapToInt(Integer::intValue).sum();
        
        // Monto el string de recuento igual que en Python (nombre:votos,nombre:votos)
        List<String> recuentoList = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : opcionesVoto.entrySet()) {
            recuentoList.add(entry.getKey() + ":" + entry.getValue());
        }
        String recuento = String.join(",", recuentoList);
        
        if (totalVotos == 0) {
            System.out.println("La urna se ha cerrado sin votos.");
            return "exito_cierre_vacio|" + recuento;
        }
        
        // Saco el máximo de votos y miro quien lo tiene (por si hay empates)
        int maxVotos = Collections.max(opcionesVoto.values());
        List<String> ganadores = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : opcionesVoto.entrySet()) {
            if (entry.getValue() == maxVotos) {
                ganadores.add(entry.getKey());
            }
        }
        
        if (ganadores.size() > 1) {
            String nombresEmpate = String.join("&", ganadores);
            System.out.println("La urna se ha cerrado con empate: " + nombresEmpate);
            return "exito_empate|" + nombresEmpate + "|" + recuento;
        } else {
            String ganador = ganadores.get(0);
            System.out.println("La urna se ha cerrado. El ganador es " + ganador);
            return "exito_cierre|" + ganador + "|" + recuento;
        }
    }
}