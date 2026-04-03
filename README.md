# Práctica: Protocolo de Votación Electrónica (Caso 14)

**Autores:** Amjad A Habeeb Mahhi y Mouad Harrouch Boukhalfa
**Asignatura:** Desarrollo de Aplicaciones en Red (DAR) - UGR

## 1. Descripción del Proyecto
En este proyecto tenemos la implementación de un sistema de votación electrónica mediante una arquitectura Cliente-Servidor usando Sockets en Python. 

El objetivo principal durante el proyecto ha sido permitir que varios clientes se conecten a la vez para emitir su voto, garantizando que nadie pueda votar dos veces (control de unicidad) y que los votos se sumen correctamente aunque dos personas voten al mismo tiempo.

## 2. Decisiones de Diseño y Arquitectura

* **Protocolo de Transporte (TCP):** Usamos TCP por el puerto 5000 porque al ser una votación no nos podemos permitir perder ningún paquete. TCP nos va a garantizar que los mensajes lleguen completos y en orden.
* **Concurrencia con Hilos:** El servidor hace uso de la librería `threading` para atender a varios clientes a la vez. Cada cliente nuevo que llega se le asigna un hilo independiente.
* **Sincronización (El Cerrojo):** Con el objetivo de evitar "Condiciones de Carrera" (que el recuento falle si dos votan a la vez), hemos usado un `Lock` (Mutex). Cuando un hilo va a sumar un voto, bloquea el acceso a las variables globales hasta que termina.
* **Estructuras de Datos:** Hemos elegido guardar el censo de votantes en un `Set` (conjunto) en vez de en una lista. Esto hace que comprobar si un DNI ya ha votado sea instantáneo. Las opciones de voto están en un diccionario.
* **Gestión de Errores:** Hemos puesto bloques `try/except` en el servidor. Si a un cliente por alguna razón se le cae el internet a mitad del proceso, el servidor no se cuelga; simplemente cierra ese socket con `finally` y sigue escuchando al resto.

## 3. Instrucciones de Ejecución

Para probar el proyecto de forma correcta hace falta usar 2 dispositivos o máquinas virtuales con Python. En nuestro caso de prueba, la IP del servidor es `192.168.1.39` y la de la máquina cliente es `192.168.1.38`.

1. Abre una terminal en la máquina del servidor y arranca el programa:
   `python codigo/servidor.py`

2. Vete a la otra máquina (la del cliente) en la misma red y arranca el programa:
   `python codigo/cliente.py`

*(Nota: Para probarlo en otros equipos, hay que asegurarse de cambiar la variable IP_SERVIDOR en el código del cliente por la IP de la nueva máquina servidora).*

## 4. El Protocolo (ABNF) y Estados
Hemos diseñado un protocolo de aplicación propio. Los mensajes son de texto plano y siempre acaban en un salto de línea (`\n`). 

El cliente se conecta solo para enviar su petición, recibe la respuesta y se desconecta rápidamente. Hay dos comandos principales:

* **VOTAR <DNI> <Candidato>:** El servidor comprueba si el DNI es válido y si no ha votado ya. Puede responder cosas como `voto_confirmado`, `dni_invalido` o `dni_ya_registrado`.
* **CERRAR:** El servidor cambia su estado a "urna cerrada". A partir de este momento rechaza nuevos votos y devuelve el recuento final (separado por barras `|`), incluyendo si hay un ganador o si hay empate.

La sintaxis exacta del protocolo está en el archivo `docs/protocolo/ABNF.txt`.

## 5. Pruebas y Análisis de Tráfico (Wireshark)
Para comprobar que el protocolo funciona bien en una red real, hemos capturado el tráfico con Wireshark ejecutando el cliente y el servidor en máquinas distintas. 

En la carpeta `pruebas/` hemos dejado:
* `captura_voto.pcap`: La captura donde se ve el saludo de TCP y cómo viajan los comandos sin fragmentarse.
* Archivos `.txt`: Diferentes pruebas que hemos hecho demostrando que el código funciona (cuando un voto va bien, cuando se intenta votar dos veces, un empate, y cuando se intenta votar con la urna cerrada).

## 6. Control de Versiones en GitHub
Para hacer el trabajo hemos usado GitHub. Hemos ido haciendo commits poco a poco para repartirnos el trabajo. Además, usamos ramas independientes (como `pruebas_wireshark`) para subir las pruebas de red y luego hicimos un *Merge / Pull Request* a la rama `main` para juntarlo todo de forma ordenada.

## 7. Estructura de Carpetas

```text
DAR_Votacion_Electronica/
├── codigo/               
│   ├── cliente.py         
│   └── servidor.py         
├── docs/                 
│   ├── protocolo/
│   │   ├── ABNF.txt       
│   │   ├── diagrama_cliente.png   
│   │   ├── diagrama_secuencia.png 
│   │   └── diagrama_servidor.png  
│   └── Memoria_Tecnica.pdf
├── pruebas/              
│   ├── captura_voto.pcap
│   ├── empate.txt      
│   ├── error_dni_repetido.txt
│   ├── seguimiento_resultados.txt
│   ├── urna_cerrada.txt        
│   └── voto_ok.txt
└── README.md
