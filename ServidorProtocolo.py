import socket
import threading

votos = {
    "CANDIDATO_A": 0, 
    "CANDIDATO_B": 0, 
    "CANDIDATO_C": 0
}
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
                        print(f"Nuevo voto para {opcion}. Recuento actual: {votos}")
                        conn.sendall(b"200 OK\r\n")
            
            elif comando == "CERRAR":
                abierto = False
                ganador = max(votos, key=votos.get)
                res_final = f"Ganador: {ganador}. Recuento final: {votos}"
                print(f"Urna cerrada. {res_final}")
                conn.sendall(f"201 {res_final}\r\n".encode('utf-8'))

    except Exception as e:
        print(f"Error en la conexion: {e}")
    finally:
        conn.close()

def iniciar():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(('0.0.0.0', 5000))
    soc.listen(5)
    print("Servidor listo. Esperando votos en el puerto 5000")
    
    while True:
        conn, addr = soc.accept()
        t = threading.Thread(target=gestionar_cliente, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    iniciar()
