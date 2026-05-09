import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.Scanner;

public class Cliente {
    public static void main(String[] args) {
        // En tu Python tenías 192.168.1.39, aquí pon la IP de la máquina de prueba
        String IP_SERVIDOR = "127.0.0.1"; 
        Scanner scanner = new Scanner(System.in);
        VotacionRemota votacion = null;

        // Intento engancharme al servidor RMI
        try {
            Registry registry = LocateRegistry.getRegistry(IP_SERVIDOR, 1099);
            votacion = (VotacionRemota) registry.lookup("ServicioVotacion");
        } catch (Exception e) {
            System.out.println("No he podido conectar (falla RMI en " + IP_SERVIDOR + ")");
            System.exit(1);
        }

        // Bucle principal de la interfaz
        while (true) {
            System.out.println("\nMenu de votacion");
            System.out.println("1. Votar ahora");
            System.out.println("2. Ver resultados y cerrar urna");
            System.out.println("3. Salir");
            System.out.print("Elige una opcion: ");
            String opcion = scanner.nextLine().trim();

            try {
                if (opcion.equals("1")) {
                    System.out.print("Dime tu DNI: ");
                    String dni = scanner.nextLine().trim();
                    System.out.println("\nCandidatos: a) Andrea Martos | b) Javier García | c) Pedro Gómez");
                    System.out.print("¿A quien quieres votar? (a/b/c): ");
                    String seleccion = scanner.nextLine().trim().toLowerCase();
                    
                    String candidato = "";
                    if (seleccion.equals("a")) candidato = "andrea_martos";
                    else if (seleccion.equals("b")) candidato = "javier_garcia";
                    else if (seleccion.equals("c")) candidato = "pedro_gomez";
                    
                    if (!candidato.isEmpty()) {
                        // Aquí llamamos al servidor como si estuviera en local, magia de RMI
                        String respuesta = votacion.emitirVoto(dni, candidato);
                        
                        // Los prints tal cual los tenías en Python
                        if (respuesta.equals("voto_confirmado")) {
                            System.out.println("Perfecto, tu voto con DNI " + dni + " se ha guardado bien.");
                        } else if (respuesta.equals("dni_ya_registrado")) {
                            System.out.println("Ese DNI ya voto antes.");
                        } else if (respuesta.equals("dni_invalido")) {
                            System.out.println("Ese DNI no vale, tienen que ser 8 numeros y una letra.");
                        } else if (respuesta.equals("urna_cerrada")) {
                            System.out.println("Llegas tarde, la urna ya esta cerrada.");
                        } else {
                            System.out.println("El servidor dice: " + respuesta);
                        }
                    } else {
                        System.out.println("Esa opcion no vale, elige a/b/c.");
                    }

                } else if (opcion.equals("2")) {
                    // Llamo a cerrar y proceso los datos como en Python
                    String res = votacion.cerrarUrna();
                    
                    if (res.startsWith("exito_cierre") || res.startsWith("exito_empate") || res.startsWith("exito_cierre_vacio")) {
                        String[] partes = res.split("\\|");
                        System.out.println("\nRecuento final de votos");
                        
                        String[] votosLista;
                        if (res.startsWith("exito_cierre_vacio")) {
                            System.out.println("No se ha registrado ningun voto , todavia no hay ganador");
                            votosLista = partes[1].split(",");
                        } else if (res.startsWith("exito_empate")) {
                            String[] nombres = partes[1].replace("_", " ").split("&");
                            System.out.println("Hay empate entre " + String.join(" y ", nombres));
                            votosLista = partes[2].split(",");
                        } else {
                            // Cambio el _ por espacio y paso a mayusculas las iniciales si hace falta
                            System.out.println("Ganador oficial: " + partes[1].replace("_", " "));
                            votosLista = partes[2].split(",");
                        }
                        
                        // Printeo el recuento
                        for (String v : votosLista) {
                            String[] candiCantidad = v.split(":");
                            System.out.println(candiCantidad[0].replace("_", " ") + ": " + candiCantidad[1] + " votos");
                        }
                    } else {
                        System.out.println("Aviso del servidor: " + res);
                    }
                    break; // Salgo despues de ver resultados

                } else if (opcion.equals("3")) {
                    break;
                } else {
                    System.out.println("Esa opcion no existe, elige 1, 2 o 3.");
                }
            } catch (RemoteException re) {
                // Manejo de errores de red 
                System.out.println("Error al comunicar con el servidor: Se ha cortado la conexion.");
            }
        }
        scanner.close();
    }
}