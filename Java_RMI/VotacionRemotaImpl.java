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
    
    private Map<String, Integer> opcionesVoto;
    private Set<String> censoVotantes;
    private volatile boolean urnaAbierta; 

    public VotacionRemotaImpl() throws RemoteException {
        super();
        this.opcionesVoto = new ConcurrentHashMap<>();
        this.opcionesVoto.put("andrea_martos", 0);
        this.opcionesVoto.put("javier_garcia", 0);
        this.opcionesVoto.put("pedro_gomez", 0);
        
        // Uso un set sincronizado para que no reviente con varios hilos
        this.censoVotantes = Collections.synchronizedSet(new HashSet<>());
        this.urnaAbierta = true;
    }

    @Override
    public String emitirVoto(String dni, String candidato) throws RemoteException {
        // Validación del DNI típica: 8 números y letra
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

        // Si el DNI ya está en el set, es que ya ha votado
        if (!censoVotantes.add(dni)) {
            return "dni_ya_registrado";
        }
        
        opcionesVoto.put(opcion, opcionesVoto.get(opcion) + 1);
        System.out.println("Voto registrado: " + dni + " -> " + opcion);
        return "voto_confirmado";
    }

    @Override
    public synchronized String cerrarUrna() throws RemoteException {
        if (!urnaAbierta) {
            return "urna_ya_cerrada_previamente";
        }
        
        urnaAbierta = false;
        int totalVotos = opcionesVoto.values().stream().mapToInt(Integer::intValue).sum();
        
        // Monto el churro de texto para el recuento
        List<String> recuentoList = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : opcionesVoto.entrySet()) {
            recuentoList.add(entry.getKey() + ":" + entry.getValue());
        }
        String recuento = String.join(",", recuentoList);
        
        if (totalVotos == 0) {
            return "exito_cierre_vacio|" + recuento;
        }
        
        // Busco el que tenga más votos y miro si hay empate
        int maxVotos = Collections.max(opcionesVoto.values());
        List<String> ganadores = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : opcionesVoto.entrySet()) {
            if (entry.getValue() == maxVotos) {
                ganadores.add(entry.getKey());
            }
        }
        
        if (ganadores.size() > 1) {
            String nombresEmpate = String.join("&", ganadores);
            return "exito_empate|" + nombresEmpate + "|" + recuento;
        } else {
            return "exito_cierre|" + ganadores.get(0) + "|" + recuento;
        }
    }
}