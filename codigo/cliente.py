import socket
import time

IP_SERVIDOR = '192.168.1.39' 

def conectar_con_servidor():
    for intento in range(1, 4):
        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(5)
            sk.connect((IP_SERVIDOR, 5000))
            return sk
        except (socket.error, socket.timeout) as e:
            print(f"No he podido conectar (Intento {intento}/3): {e}")
            if intento < 3:
                time.sleep(2)
    return None

def ejecutar_interfaz():
    while True:
        print("\nMenu de votacion")
        print("1. Votar ahora")
        print("2. Ver resultados y cerrar urna")
        print("3. Salir")
        
        opcion = input("Elige una opcion: ").strip()

        if opcion == '1':
            dni = input("Dime tu DNI: ").strip()
            print("\nCandidatos: a) Andrea Martos | b) Javier García | c) Pedro Gómez")
            seleccion = input("¿A quien quieres votar? (a/b/c): ").strip().lower()
            mapeo = {'a': 'andrea_martos', 'b': 'javier_garcia', 'c': 'pedro_gomez'}
            
            if seleccion in mapeo:
                s = conectar_con_servidor()
                if s:
                    try:
                        s.sendall(f"VOTAR {dni} {mapeo[seleccion]}\n".encode('utf-8'))
                        respuesta = s.recv(1024).decode('utf-8').strip()
                        s.close()
                        
                        if "voto_confirmado" in respuesta:
                            print(f"Perfecto, tu voto con DNI {dni} se ha guardado bien.")
                            break
                        elif "dni_ya_registrado" in respuesta:
                            print("Ese DNI ya voto antes.")
                        elif "dni_invalido" in respuesta:
                            print("Ese DNI no vale, tienen que ser 8 numeros y una letra.")
                        elif "urna_cerrada" in respuesta:
                            print("Llegas tarde, la urna ya esta cerrada.")
                        else:
                            print(f"El servidor dice: {respuesta}")
                    except socket.error as e:
                        print(f"Error al enviar el voto: {e}")
            else:
                print("Esa opcion no vale, elige a/b/c.")

        elif opcion == '2':
            s = conectar_con_servidor()
            if s:
                try:
                    s.sendall(b"CERRAR\n")
                    res = s.recv(1024).decode('utf-8').strip()
                    s.close()
                    
                    if "exito_cierre" in res or "exito_cierre_vacio" in res or "exito_empate" in res:
                        partes = res.split('|')
                        print("\nRecuento final de votos")
                        
                        if "exito_cierre_vacio" in res:
                            print("No se ha registrado ningun voto , todavia no hay ganador")
                            votos_lista = partes[1].split(',')
                        elif "exito_empate" in res:
                            nombres = partes[1].replace('_', ' ').title().split('&')
                            print(f"Hay empate entre {' y '.join(nombres)}")
                            votos_lista = partes[2].split(',')
                        else:
                            print(f"Ganador oficial: {partes[1].replace('_', ' ').title()}")
                            votos_lista = partes[2].split(',')
                        
                        for v in votos_lista:
                            candi, cantidad = v.split(':')
                            print(f"{candi.replace('_',' ').title()}: {cantidad} votos")
                    else:
                        print(f"Aviso del servidor: {res}")
                    break
                except socket.error as e:
                    print(f"Error al pedir el cierre: {e}")
            
        elif opcion == '3':
            break
        
        else:
            print("Esa opcion no existe, elige 1, 2 o 3.")

ejecutar_interfaz()
