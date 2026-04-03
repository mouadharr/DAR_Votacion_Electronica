# Práctica: Protocolo de Votación Electrónica (Caso 14)

**Autores:** Amjad A Habeeb Mahhi y Mouad Harrouch Boukhalfa  
**Asignatura:** Desarrollo de Aplicaciones en Red (DAR) - 3º GITT - UGR

---

## 1. Descripción del Proyecto
Este proyecto implementa un sistema de votación electrónica basado en una arquitectura **Cliente-Servidor** mediante la API de sockets de Python. 

El objetivo principal ha sido permitir que varios clientes se conecten a la vez para emitir su voto, garantizando que nadie pueda votar dos veces (control de unicidad) y que los votos se sumen correctamente aunque dos personas voten al mismo tiempo.

---

## 2. Decisiones de Diseño y Arquitectura

* **Protocolo de Transporte (TCP):** Usamos TCP por el puerto **5000** porque al ser una votación no nos podemos permitir perder ningún paquete. TCP nos garantiza que los mensajes lleguen completos, en orden y que la conexión sea fiable.
* **Concurrencia con Hilos:** El servidor hace uso de la librería `threading` para atender a varios clientes a la vez. Cada cliente nuevo que llega se le asigna un hilo independiente para no bloquear el servicio.
* **Sincronización (El Cerrojo):** Con el objetivo de evitar "Condiciones de Carrera" (que el recuento falle si dos personas votan a la vez), hemos usado un **Lock (Mutex)**. Cuando un hilo va a sumar un voto, bloquea el acceso a las variables globales hasta que termina su operación.
* **Estructuras de Datos:** * **Censo:** Guardamos los DNIs en un **set()** (conjunto), lo que hace que comprobar si alguien ya ha votado sea instantáneo (complejidad O(1)).
    * **Urna:** Las opciones de voto se gestionan en un diccionario para un procesamiento rápido.
* **Gestión de Errores:** Hemos blindado el código con bloques `try/except/finally`. Si a un cliente se le cae el internet o hay un error inesperado, el servidor no se cuelga; cierra ese socket de forma segura y sigue escuchando al resto.

---

## 3. El Protocolo (ABNF) y Estados
Hemos diseñado un protocolo de aplicación propio con mensajes de texto plano que terminan siempre en salto de línea (`\n`).

* **VOTAR <DNI> <Candidato>:** El servidor comprueba si el DNI es válido y si no ha votado ya. Responde con confirmaciones o errores como `dni_ya_registrado`.
* **CERRAR:** Orden exclusiva para finalizar la votación. El servidor pasa al **Estado H** (urna cerrada), bloquea nuevos votos y devuelve el recuento final detallado.

La especificación formal y los diagramas de comportamiento se encuentran en la carpeta `docs/`.

---

## 4. Validación en Red Real (Wireshark)
Para comprobar que el protocolo funciona bien en una red real, hemos capturado el tráfico con Wireshark ejecutando el cliente y el servidor en máquinas distintas (IPs `.38` y `.39`).

En la carpeta `pruebas/` se encuentran los **5 archivos PCAP** con los casos de prueba. Para revisar el contenido de los mensajes se debe usar la función **"Seguir secuencia TCP" (Follow TCP Stream)**:

1. **`voto_ok.pcap`**: Flujo de una votación estándar completada con éxito.
2. **`error_dni_repetido.pcap`**: Demostración de integridad donde el servidor detecta un DNI duplicado.
3. **`empate.pcap`**: Caso de cierre de urna con múltiples ganadores y recuento detallado.
4. **`seguimiento_resultados.pcap`**: Captura del proceso de cierre y recepción del acta final.
5. **`urna_cerrada.pcap`**: Prueba de robustez donde el servidor rechaza votos tras el cierre.

---

## 5. Control de Versiones en GitHub
Hemos mantenido un historial de commits progresivo para repartirnos el trabajo de forma equilibrada. Se han utilizado **ramas independientes** para las pruebas de red y validación antes de integrar los cambios definitivos en la rama `main`.

---

## 6. Instrucciones de Ejecución
1. Lanzar el servidor: `python Votacion_Electronica/codigo/servidor.py`
2. Lanzar el cliente: `python Votacion_Electronica/codigo/cliente.py`

---

## 7. Estructura del Proyecto

```text
DAR-Proyecto-Votacion-Electronica/
├── README.md
└── Votacion_Electronica/
    ├── codigo/
    │   ├── cliente.py
    │   └── servidor.py
    ├── docs/
    │   ├── diagramas/
    │   ├── memoria_diseño/
    │   └── protocolo/
    └── pruebas/
        ├── voto_ok.pcap
        ├── error_dni_repetido.pcap
        ├── empate.pcap
        ├── seguimiento_resultados.pcap
        └── urna_cerrada.pcap
