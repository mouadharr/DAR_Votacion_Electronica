import socket
import threading

votos = {"OPCION1": 0, "OPCION2": 0}
censados = set()
abierto = True
cerrojo = threading.Lock()

def gestionar_cliente(conn, addr):
    global abierto
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        if not data: return
        
        partes = data.split(' ')
        comando = partes[0]

        with cerrojo:
            if comando == "VOTAR":
                if not abierto:
                    conn.sendall(b"403 ERROR_CERRADO\r\n")
                else:
                    dni, opcion = partes[1], partes[2]
                    if dni in censados:
                        conn.sendall(b"601 YA_VOTADO\r\n")
                    else:
                        censados.add(dni)
                        votos[opcion] += 1
                        conn.sendall(b"200 OK\r\n")
            
            elif comando == "CERRAR":
                abierto = False
                conn.sendall(b"201 Votacion finalizada\r\n")
    finally:
        conn.close()

def iniciar():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(('0.0.0.0', 5000))
    soc.listen(5)
    print("Servidor activo puerto 5000")
    
    while True:
        c, a = soc.accept()
        threading.Thread(target=gestionar_cliente, args=(c, a)).start()

iniciar()
