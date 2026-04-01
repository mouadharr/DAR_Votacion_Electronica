# Caso 14: Protocolo de Votación Electrónica (Proyecto DAR)

## 1. Visión General del Sistema
En este proyecto se desarrolla un servicio de red de nivel de aplicación para la gestión de votaciones implementado con una arquitectura Cliente-Servidor. El sistema permite la recepción de varios votos a la vez, valida la identidad del electorado y garantiza un recuento de votos final consistente mediante técnicas de programación concurrente.

## 2. Fundamentos de la Arquitectura
* **Protocolo de Transporte:** Empleamos **TCP** (puerto 5000), gracias a esto , se proporciona un canal de comunicación orientado a conexión que garantiza que cada voto llegue sin errores y de forma completamente ordenada.
* **Gestión de la Concurrencia:** El servidor hace uso de la librería `threading` de Python para atender a múltiples terminales de voto a la vez. El acceso a la urna digital se protege mediante un **Mutex (Lock)** para que no se produzcan condiciones de carrera durante la actualización del recuento de votos.
* **Política de Censo:** Se integra un registro dinámico de votantes en memoria que valida el formato del DNI y bloquea intentos de doble sufragio en tiempo real.

## 3. Entorno de Ejecución
* **Runtime:** Python 3.10 o superior.
* **Dependencias:** Hacemos uso exclusivamente de la API nativa de red (socket, threading, time), de esta manera se facilita su portabilidad sin instalaciones externas.
* **Infraestructura:** Optimizado para despliegues LAN sobre máquinas físicas o virtuales. 

## 4. Guía de Despliegue y Operación
Para asegurar la integridad de las rutas de archivos, es aconsejable ejecutar los módulos desde el directorio raíz:

### ◦ Escenario de Simulación (Local)
1. Iniciar Servidor de Urna: `python codigo/servidor.py`
2. Iniciar Terminal de Voto: `python codigo/cliente.py`

### ◦ Escenario de Operación en Red
Configurar la dirección IPv4 de la máquina del servidor en la variable correspondiente del script `cliente.py` para establecer la visibilidad entre hosts.

## 5. Primitivas del Protocolo de Aplicación
Al haber hecho uso de python hemos implementado el código de manera que los mensajes se intercambian en formato ASCII delimitados por un salto de línea (LF). 

| Primitiva | Sintaxis del Mensaje | Propósito Funcional | Respuesta del Servidor |
| :--- | :--- | :--- | :--- |
| **VOTAR** | `VOTAR <DNI> <CANDIDATO>` | Transmisión de papeleta digital | `voto_confirmado` |
| **CERRAR** | `CERRAR` | Finalización de jornada y recuento | `exito_cierre\|ganador\|lista` |
| **STATUS** | (Mecanismo interno) | Notificación de error o duplicidad | `dni_ya_registrado` |

La especificación gramatical formal se encuentra en `docs/protocolo/ABNF.txt`.

## 6. Jerarquía del Repositorio
Organización del proyecto:

```text
📂 DAR_Votacion_Electronica/
├── 📂 codigo/              # Código fuente (Servicios de red)
│   ├── cliente.py          # Terminal de voto 
│   └── servidor.py         # Gestión de multihilo
├── 📂 docs/                # Documentación
│   ├── 📂 protocolo/
│   │   ├── ABNF.txt        # Especificación gramatical formal
│   │   ├── Diagrama_secuencia.png # Interacción temporal
│   │   ├── diagrama_cliente.png   # FSM Cliente
│   │   └── diagrama_servidor.png  # FSM Servidor
├── 📂 pruebas/             # Evidencias de auditoría en red
│   ├── captura_voto.pcap      # Captura de tráfico Wireshark
│   └── flujo_datos.png        # Análisis de PDU (Follow TCP Stream)
└── 📄 README.md            # Documento técnico principal
