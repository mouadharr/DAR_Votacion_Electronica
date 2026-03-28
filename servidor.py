import socket
import threading

votos = {"ANDREA_MARTOS": 0, "JAVIER_GARCIA": 0, "PEDRO_GOMEZ": 0}
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
                    dni = partes[1]
                    opcion = partes[2]
                    
                    if opcion not in votos:
                        conn.sendall(b"404 OPCION_INVALIDA\r\n")
                    elif dni in censados:
                        conn.sendall(b"601 YA_VOTADO\r\n")
                    else:
                        censados.add(dni)
                        votos[opcion] += 1
                        conn.sendall(b"200 OK\r\n")
            
            elif comando == "CERRAR":
                abierto = False
                ganador = max(votos, key=votos.get)
                res_final = f"Ganador: {ganador}. Recuento final: {votos}"
                conn.sendall(f"201 {res_final}\r\n".encode('utf-8'))

    except Exception:
        pass
    finally:
        conn.close()

def iniciar():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(('0.0.0.0', 5000))
    soc.listen(5)
    while True:
        conn, addr = soc.accept()
        threading.Thread(target=gestionar_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    iniciar()
