import socket
import threading

opciones_voto = {"andrea_martos": 0, "javier_garcia": 0, "pedro_gomez": 0}
censo_votantes = set()
urna_abierta = True
cerrojo = threading.Lock()
hilos_vivos = []

def registrar_voto_en_censo(identificador, candidato):
    if len(identificador) != 9 or not identificador[:8].isdigit() or not identificador[-1].isalpha():
        return "dni_invalido"
    
    opcion = candidato.lower()
    if opcion not in opciones_voto:
        return "candidato_inexistente"
    
    if identificador in censo_votantes:
        return "dni_ya_registrado"
    
    censo_votantes.add(identificador)
    opciones_voto[opcion] += 1
    print(f"Voto de {identificador} para {opcion} registrado correctamente")
    return "voto_confirmado"

def gestionar_peticion(conexion, direccion):
    global urna_abierta
    try:
        mensaje = conexion.recv(1024).decode('utf-8').strip()
        if mensaje:
            print(f"Peticion de {direccion}: {mensaje}")
            elementos = mensaje.split()
            if elementos:
                orden = elementos[0].upper()
                with cerrojo:
                    if orden == "VOTAR" and len(elementos) >= 3:
                        if urna_abierta:
                            resultado = registrar_voto_en_censo(elementos[1], elementos[2])
                            conexion.sendall(f"{resultado}\n".encode('utf-8'))
                        else:
                            conexion.sendall(b"urna_cerrada\n")
                    elif orden == "CERRAR":
                        if urna_abierta:
                            urna_abierta = False
                            total_votos = sum(opciones_voto.values())
                            recuento = ",".join([f"{k}:{v}" for k, v in opciones_voto.items()])
                            
                            if total_votos == 0:
                                print("La urna se ha cerrado sin votos.")
                                conexion.sendall(f"exito_cierre_vacio|{recuento}\n".encode('utf-8'))
                            else:
                                max_votos = max(opciones_voto.values())
                                ganadores = [k for k, v in opciones_voto.items() if v == max_votos]
                                
                                if len(ganadores) > 1:
                                    nombres_empate = "&".join(ganadores)
                                    print(f"La urna se ha cerrado con empate: {nombres_empate}")
                                    conexion.sendall(f"exito_empate|{nombres_empate}|{recuento}\n".encode('utf-8'))
                                else:
                                    ganador = ganadores[0]
                                    print(f"La urna se ha cerrado. El ganador es {ganador}")
                                    conexion.sendall(f"exito_cierre|{ganador}|{recuento}\n".encode('utf-8'))
                        else:
                            conexion.sendall(b"urna_ya_cerrada_previamente\n")
                    else:
                        conexion.sendall(b"comando_invalido\n")
    except socket.error as e:
        print(f"Error en la comunicacion con {direccion}: {e}")
    except Exception as e:
        print(f"Se ha producido un error al procesar la peticion: {e}")
    finally:
        conexion.close()

def iniciar_servidor():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.bind(('0.0.0.0', 5000))
        serv.listen(10)
        print("Servidor activo. Esperando en el puerto 5000...")
        
        while True:
            canal, addr = serv.accept()
            hilo = threading.Thread(target=gestionar_peticion, args=(canal, addr))
            hilos_vivos.append(hilo)
            hilo.start()
    except Exception as e:
        print(f"No se ha podido iniciar el servidor correctamente: {e}")
    finally:
        serv.close()

iniciar_servidor()
