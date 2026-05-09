import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.Scanner;

public class Cliente {
    public static void main(String[] args) {
        // IP de la máquina donde esté el servidor (localhost para probar)
        String IP_SERVIDOR = "127.0.0.1"; 
        Scanner scanner = new Scanner(System.in);
        VotacionRemota votacion = null;

        try {
            Registry registry = LocateRegistry.getRegistry(IP_SERVIDOR, 1099);
            votacion = (VotacionRemota) registry.lookup("ServicioVotacion");
        } catch (Exception e) {
            System.out.println("Error: No se encuentra el servidor en " + IP_SERVIDOR);
            System.exit(1);
        }

        while (true) {
            System.out.println("\n--- Votaciones ---");
            System.out.println("1. Votar");
            System.out.println("2. Cerrar urna y ver resultados");
            System.out.println("3. Salir");
            System.out.print("Opcion: ");
            String opcion = scanner.nextLine().trim();

            try {
                if (opcion.equals("1")) {
                    System.out.print("DNI: ");
                    String dni = scanner.nextLine().trim();
                    System.out.println("\nCandidatos: a) Andrea | b) Javier | c) Pedro");
                    System.out.print("Voto (a/b/c): ");
                    String seleccion = scanner.nextLine().trim().toLowerCase();
                    
                    String candidato = "";
                    if (seleccion.equals("a")) candidato = "andrea_martos";
                    else if (seleccion.equals("b")) candidato = "javier_garcia";
                    else if (seleccion.equals("c")) candidato = "pedro_gomez";
                    
                    if (!candidato.isEmpty()) {
                        // Invocación remota (la magia de RMI)
                        String respuesta = votacion.emitirVoto(dni, candidato);
                        
                        if (respuesta.equals("voto_confirmado")) {
                            System.out.println("Voto guardado.");
                        } else if (respuesta.equals("dni_ya_registrado")) {
                            System.out.println("Ya has votado con este DNI.");
                        } else if (respuesta.equals("dni_invalido")) {
                            System.out.println("Formato de DNI incorrecto.");
                        } else if (respuesta.equals("urna_cerrada")) {
                            System.out.println("Demasiado tarde, urna cerrada.");
                        } else {
                            System.out.println("Server dice: " + respuesta);
                        }
                    } else {
                        System.out.println("Esa opción no es válida.");
                    }

                } else if (opcion.equals("2")) {
                    String res = votacion.cerrarUrna();
                    
                    if (res.contains("exito")) {
                        String[] partes = res.split("\\|");
                        System.out.println("\n--- RECUENTO ---");
                        
                        if (res.startsWith("exito_cierre_vacio")) {
                            System.out.println("No hay votos en la urna.");
                        } else if (res.startsWith("exito_empate")) {
                            System.out.println("Empate entre: " + partes[1].replace("_", " "));
                        } else {
                            System.out.println("Ganador: " + partes[1].replace("_", " "));
                        }
                        
                        String[] votosLista = partes[partes.length - 1].split(",");
                        for (String v : votosLista) {
                            String[] data = v.split(":");
                            System.out.println(data[0].replace("_", " ") + ": " + data[1]);
                        }
                    }
                    break; 

                } else if (opcion.equals("3")) {
                    break;
                }
            } catch (RemoteException re) {
                System.out.println("Se ha perdido la conexión con el servidor.");
                break;
            }
        }
        scanner.close();
    }
}