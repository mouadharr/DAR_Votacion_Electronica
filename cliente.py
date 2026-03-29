import socket
import time

ip_del_servidor = '192.168.1.39' 

def intentar_conectar():
    intentos = 0
    while intentos < 3:
        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(3)
            sk.connect((ip_del_servidor, 5000))
            return sk
        except (ConnectionRefusedError, socket.timeout):
            intentos += 1
            print(f"reintentando conexion... {intentos}")
            time.sleep(1)
        except Exception as e:
            break
    return None

def menu():
    while True:
        print("\n--- menu votacion ---")
        print("1. votar")
        print("2. cerrar y ver resultados")
        print("3. salir")
        
        op = input("elige una opcion: ").strip()

        if op == '1':
            dni = input("dime tu dni: ").strip()
            if len(dni) < 5 or " " in dni:
                print("has escrito mal el dni")
                continue

            print("\nselecciona candidato:")
            print("a. andrea_martos")
            print("b. javier_garcia")
            print("c. pedro_gomez")
            
            sel = input("tu eleccion (a/b/c): ").strip().lower()
            mapping = {'a': 'andrea_martos', 'b': 'javier_garcia', 'c': 'pedro_gomez'}
            
            if sel not in mapping:
                print("esa letra no vale")
                continue
                
            nom = mapping[sel]
            s = intentar_conectar()
            if s is None:
                print("el servidor no responde")
                continue

            try:
                s.sendall(f"votar {dni} {nom}\n".encode('utf-8'))
                respuesta = s.recv(1024).decode('utf-8').strip()
                s.close()

                if "voto_registrado" in respuesta:
                    print(f"gracias {dni}, tu voto a {nom} ha sido registrado")
                    break
                else:
                    print(f"el servidor dice: {respuesta}")
            except Exception as e:
                print("error al enviar")

        elif op == '2':
            s = intentar_conectar()
            if s:
                try:
                    s.sendall(b"cerrar\n")
                    respuesta_final = s.recv(1024).decode('utf-8').strip()
                    print(f"la urna se ha cerrado: {respuesta_final}")
                    s.close()
                    break
                except Exception as e:
                    print("error al cerrar")
            
        elif op == '3':
            print("saliendo...")
            break
        else:
            print("opcion no existe")

if __name__ == "__main__":
    menu()
