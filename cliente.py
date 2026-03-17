import socket

def mandar():
    host = input("¿A qué IP nos conectamos? ")
    print("¿Qué quieres hacer?\n1. Votar\n2. Ver cómo va el recuento\n3. Terminar la votación")
    op = input("Elige una opción: ")

    try:
        f = socket.AF_INET
        t = socket.SOCK_STREAM
        
        with socket.socket(f, t) as s:
            s.connect((host, 5000))
            
            if op == "1":
                dni = input("DNI: ")
                voto = input("¿A quién votas? (OPCION1 o OPCION2): ")
                msg = "VOTAR " + dni + " " + voto + "\r\n"
            elif op == "2":
                msg = "RESULTADOS\r\n"
            elif op == "3":
                msg = "CERRAR\r\n"
            else:
                print("Esa opción no existe.")
                return

            s.sendall(msg.encode())
            data = s.recv(1024).decode()
            print("El servidor responde:", data)
            
    except:
        print(" No se ha podido conectar con el servidor.")

mandar()