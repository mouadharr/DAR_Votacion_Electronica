import socket

def enviar_voto():
    destino_ip = '192.168.1.XX' 
    puerto = 5000

    print("SISTEMA DE VOTOS")
    id_usuario = input("DNI: ")
    opcion = input("Voto (OPCION1/OPCION2): ")

    msg = f"VOTAR {id_usuario} {opcion}\r\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((destino_ip, puerto))
        s.sendall(msg.encode('utf-8'))
        
        respuesta = s.recv(1024).decode('utf-8')
        print(f"Resultado: {respuesta}")
        s.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    enviar_voto()
