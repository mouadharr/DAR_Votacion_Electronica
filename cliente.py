import socket

def menu():
    print("\n1. ANDREA_MARTOS\n2. JAVIER_GARCIA\n3. PEDRO_GOMEZ\n4. CERRAR URNA")
    return input("Opción: ")

def enviar(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.1.39', 5000))
        s.sendall(f"{msg}\r\n".encode('utf-8'))
        resp = s.recv(1024).decode('utf-8')
        s.close()
        return resp
    except Exception as e:
        return str(e)

def main():
    while True:
        opc = menu()
        if opc in ['1', '2', '3']:
            dni = input("DNI: ")
            cands = {'1':"ANDREA_MARTOS", '2':"JAVIER_GARCIA", '3':"PEDRO_GOMEZ"}
            res = enviar(f"VOTAR {dni} {cands[opc]}")
            
            if "200 OK" in res:
                print("Voto registrado correctamente.")
                break
            elif "601" in res:
                print("Error: Este DNI ya ha votado.")
            else:
                print(f"Error: {res}")
                break
                
        elif opc == '4':
            print(f"Resultado: {enviar('CERRAR')}")
            break

if __name__ == "__main__":
    main()
