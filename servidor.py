import socket
import threading

opciones_voto = {"andrea_martos": 0, "javier_garcia": 0, "pedro_gomez": 0}
dni_registrados = set()
urna_activa = True
bloqueo = threading.Lock()

def validar_y_contar(dni, candidato):
    if " " in dni or len(dni) < 5:
        return "dni_incorrecto"
    
    nom = candidato.lower()
    if nom not in opciones_voto:
        return "ese_nombre_no_vale"
    
    if dni in dni_registrados:
        return "ya_has_votado"
    
    dni_registrados.add(dni)
    opciones_voto[nom] += 1
    print(f"voto de {dni} para {nom} ok")
    return "voto_registrado"

def atender_peticion(s, addr):
    global urna_activa
    try:
        data = s.recv(1024).decode('utf-8').strip()
        if not data:
            return

        print(f"peticion de {addr}: {data}")
        partes = data.split(' ')
        cmd = partes[0].lower()

        with bloqueo:
            if cmd == "votar":
                if not urna_activa:
                    s.sendall(b"lo_siento_la_urna_esta_cerrada\n")
                elif len(partes) < 3:
                    s.sendall(b"faltan_datos_en_el_mensaje\n")
                else:
                    res = validar_y_contar(partes[1], partes[2])
                    s.sendall(f"{res}\n".encode('utf-8'))

            elif cmd == "cerrar":
                if not urna_activa:
                    s.sendall(b"la_urna_ya_estaba_cerrada\n")
                else:
                    urna_activa = False
                    ganador = max(opciones_voto, key=opciones_voto.get)
                    puntos = ",".join([f"{k}:{v}" for k, v in opciones_voto.items()])
                    print(f"urna cerrada. el ganador es {ganador}")
                    s.sendall(f"urna_cerrada_ganador_{ganador}_votos_{puntos}\n".encode('utf-8'))
            else:
                s.sendall(b"comando_desconocido\n")
    except Exception as e:
        print(f"error con el cliente {addr}")
    finally:
        s.close()

def iniciar():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        serv.bind(('0.0.0.0', 5000))
        serv.listen(5)
        print("esperando en el 5000")
        
        while True:
            c, addr = serv.accept()
            t = threading.Thread(target=atender_peticion, args=(c, addr))
            t.daemon = True
            t.start()
    except Exception as e:
        print("error en el server")
    finally:
        serv.close()

if __name__ == "__main__":
    iniciar()
