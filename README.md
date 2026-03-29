PROTOCOLO DE VOTACIÓN ELECTRÓNICA 

Autores:

-Mouad Harrouch Boukhalfa

-Amjad A Habeeb Mahhi

En este repositorio tenemos la implementación de un servidor cliente-servidor con  el objetivo de gestionar procesos de votación electrónica . Este sistema garantiza que cada votante pueda votar una única vez y permite el cierre formal con resultados detallados .


1. Descripción del Protocolo

Este protocolo permite la comunicación entre múltiples clientes y un servidor para emitir votos sobre opciones predefinidas. El servidor controla el censo de votantes para evitar duplicados y gestiona la transición de la urna de estado abierto a cerrado.

Características técnicas:

-Delimitación de mensajes: Se realiza de forma manual mediante el salto de línea (\n) para separar los datos

-Validación: El servidor comprueba la validez de la opción elegida antes de procesar el voto.

-Gestión de errores: Se han definido respuestas específicas para casos de DNI repetido, urna que no sigue abierta o comandos mal escritos.

2. Arquitectura y Transporte

-Protocolo de transporte: Se usa TCP en el puerto 5000. Se ha elegido este protocolo para facilitar el mantenimiento de la conexión y el correcto envío de los mensajes.

-Concurrencia: El servidor es multihilo, para ello usamos la biblioteca threading para gestionar solicitudes simultáneas sin que ocurra un bloqueo cuando dos personajes o más hagan varias 
solicitudes a la vez.

-Exclusión mutua: Hemos implementado bloqueos (Lock) para que solo un hilo pueda modificar el recuento de votos a la vez. Esto evita que si dos cliente votan a la vez sus actualizaciones choquen .

3. Guía de Ejecución
   
Configuración

En el archivo cliente.py, se debe cambiar la dirección IP del servidor. En nuestro caso las direcciones IP son :

-IP Servidor: 192.168.1.39

-IP Cliente: 192.168.1.38

Comandos 

Servidor: Iniciar en la máquina receptora :

python3 servidor.py

Cliente: Iniciar en la máquina emisora :

python3 cliente.py

4. Validación en Red

La comunicación la hemos validado mediante capturas de tráfico real entre dos máquinas virtuales distintas ejecutadas desde el mismo equipo . El archivo de captura se encuentra en la carpeta /docs/captura.pcap.

En wireshark hemos analizado : 

- Handshake TCP: Se observa el establecimiento de la conexión  entre la IP .38 y la IP .39.

- Intercambio de datos: Se identifican los mensajes PSH/ACK correspondientes a los comandos de voto y las confirmaciones que da el  servidor.

- Cierre de conexión: Finalización de la comunicación mediante el intercambio de flags FIN/ACK.

  
5. Documentación de Diseño Formal
La especificación completa del protocolo se encuentra en formato en el archivo memoria.pdf dentro de la carpeta /docs. Este documento incluye:

-ABNF.

-Diagramas de estados.

-Diagramas de secuencia.

-Gestión de errores .



