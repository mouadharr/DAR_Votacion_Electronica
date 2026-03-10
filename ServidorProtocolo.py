import socket
IP = '0.0.0.0'
PUERTO = 5000
listavotantes = []

def empezar():
    # Abrimos el enchufe de red
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as enchufe:
        enchufe.bind((IP, PUERTO))
        enchufe.listen()
        print("Servidor en marcha")

        while True:
            # Aceptamos al que llega atravesando el canal
            canal, cliente = enchufe.accept()
            with canal:
                # Leemos el texto que nos da
                texto = canal.recv(1024).decode('utf-8')
                if not texto: continue
                datos = texto.strip().split(' ')
                orden = datos[0]
                dni = datos[1] if len(datos) > 1 else ""
                
                if orden == "REG_VOT":
                    if dni in listavotantes:
                        canal.sendall(b"601 DENEGADO\r\n")
                        print("DNI repetido")
                    else:
                        listavotantes.append(dni)
                        canal.sendall(b"100 AUTORIZADO\r\n")
                        print("Voto guardado")

empezar()