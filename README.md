# Caso 14: Protocolo de Votación Electrónica (Proyecto DAR)

## 1. Visión General del Sistema
En este proyecto se desarrolla un servicio de red de nivel de aplicación para la gestión de votaciones implementado con una arquitectura Cliente-Servidor. El sistema permite la recepción de varios votos a la vez, valida la identidad del electorado y garantiza un recuento de votos final consistente mediante técnicas de programación concurrente.

## 2. Fundamentos de la Arquitectura
Protocolo de Transporte: Empleamos TCP (puerto 5000), gracias a esto, se proporciona un canal de comunicación orientado a conexión que garantiza que cada voto llegue sin errores y de forma completamente ordenada.

Gestión de la Concurrencia: El servidor hace uso de la librería threading de Python para atender a múltiples terminales de voto a la vez. El acceso a la urna digital se protege mediante un Mutex (Lock) para que no se produzcan condiciones de carrera durante la actualización del recuento de votos.

Política de Censo: Se integra un registro dinámico de votantes en memoria que valida el formato del DNI y bloquea intentos de doble sufragio en tiempo real.

## 3. Entorno de Ejecución
Runtime: Python 3.10 o superior.

Dependencias: Hacemos uso exclusivamente de la API nativa de red (socket, threading, time), de esta manera se facilita su portabilidad sin instalaciones externas.

Infraestructura: Optimizado para despliegues LAN sobre máquinas físicas o virtuales.

## 4. Guía de Despliegue y Operación
Para asegurar la integridad de las rutas de archivos, es aconsejable ejecutar los módulos desde el directorio raíz:

### Escenario de Simulación (Local)
1. Iniciar Servidor de Urna: python codigo/servidor.py
2. Iniciar Terminal de Voto: python codigo/cliente.py

### Escenario de Operación en Red
Configurar la dirección IPv4 de la máquina del servidor en la variable correspondiente del script cliente.py para establecer la visibilidad entre hosts.

## 5. Primitivas del Protocolo de Aplicación
Al haber hecho uso de python hemos implementado el código de manera que los mensajes se intercambian en formato ASCII delimitados por un salto de línea (LF).

| Primitiva | Sintaxis del Mensaje | Propósito Funcional | Respuesta del Servidor |
| :--- | :--- | :--- | :--- |
| **VOTAR** | `VOTAR <DNI> <CANDIDATO>` | Transmisión de papeleta digital | `voto_confirmado` |
| **CERRAR** | `CERRAR` | Finalización de jornada y recuento | `exito_cierre\|ganador\|lista` |
| **STATUS** | (Mecanismo interno) | Notificación de error o duplicidad | `dni_ya_registrado` |

La especificación gramatical formal se encuentra en docs/protocolo/ABNF.txt.

## 6. Validación y Auditoría de Tráfico (Wireshark)
Con el objetivo de cumplir con los requisitos de validación en red, se ha analizado cómo se comporta el protocolo mediante el análisis de trazas capturadas con Wireshark durante la simulación. Las pruebas se realizaron en una red local entre dos máquinas virtuales con sistema operativo Linux (Cliente: 192.168.1.38 y Servidor: 192.168.1.39).

### Análisis de la Captura (.pcap)
Se adjunta el archivo captura_voto.pcap en la carpeta de pruebas como evidencia técnica de los siguientes puntos:

Establecimiento de sesión: Handshake TCP completo (SYN, SYN-ACK, ACK) antes del intercambio de datos.

Cumplimiento ABNF: Verificación de que las unidades de datos (PDUs) siguen la sintaxis diseñada para el protocolo.

Delimitación de mensajes: Uso del carácter de salto de línea para evitar problemas de fragmentación en la lectura del socket.

### Ejemplos de Verificación del Protocolo
En la carpeta de pruebas se incluyen escenarios representativos para verificar que la lógica del servidor se ha implementado correctamente. Los flujos de datos de estos ejemplos se encuentran en formato de texto:

**Voto Procesado con Éxito (voto_ok.txt)**
¿Qué vemos?: Un votante con DNI 12345678Z envía un voto para la candidata Andrea Martos.
¿Qué hace el código?: El servidor bloquea el acceso al fichero mediante un cerrojo (Lock) para evitar escrituras simultáneas, registra el voto y confirma que se ha guardado correctamente.

**Intento de Voto Duplicado (error_dni_repetido.txt)**
¿Qué vemos?: El mismo DNI intenta votar otra vez.
¿Qué hace el código?: El servidor consulta su lista de control, detecta que el identificador ya existe y rechaza la petición enviando un mensaje de error para asegurar la unicidad del voto.

**Consulta de Resultados (seguimiento_resultados.txt)**
¿Qué vemos?: El cliente solicita ver el estado actual del recuento.
¿Qué hace el código?: El servidor suma los votos almacenados y envía el total actualizado al cliente de forma íntegra.

**Urna Cerrada (urna_cerrada.txt)**
¿Qué vemos?: Un intento de votación (VOTAR 12345678B andrea_martos) cuando el periodo de votación ya ha acabado.
¿Qué hace el código?: El servidor identifica que el estado de la urna es inactivo y responde con "urna_cerrada", impidiendo la entrada de votos fuera de tiempo.

**Situación de Empate (empate.txt)**
¿Qué vemos?: La petición de cierre (CERRAR) cuando existe una igualdad de votos entre candidatos.
¿Qué hace el código?: El servidor detecta el empate entre Andrea Martos y Javier García (1 voto cada uno) y genera un mensaje de los ganadores empatados y el desglose final .

## 7. Jerarquía del Repositorio
Organización del proyecto:

```text
DAR_Votacion_Electronica/
├── codigo/               
│   ├── cliente.py         
│   └── servidor.py         
├── docs/                 
│   ├── protocolo/
│   │   ├── ABNF.txt       
│   │   ├── Diagrama_secuencia.png 
│   │   ├── diagrama_cliente.png   
│   │   └── diagrama_servidor.png  
│   └── Memoria_Tecnica.pdf
├── pruebas/              
│   ├── captura_voto.pcap      
│   ├── voto_ok.txt
│   ├── error_dni_repetido.txt
│   └── seguimiento_resultados.txt        
└── README.md







