import asyncio
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Sistema de Votación REST",
    description="API REST para el Caso 14: Protocolo de votación electrónica con control de unicidad y cierre formal.",
    version="1.0.0"
)

# --- Estado Global en Memoria ---
opciones_voto = {
    "andrea_martos": 0,
    "javier_garcia": 0,
    "pedro_gomez": 0
}
censo_votantes = set()
urna_abierta = True
cerrojo = asyncio.Lock()  # Lock para concurrencia segura

# --- Modelos Pydantic ---
class VotoCreate(BaseModel):
    dni: str
    candidato: str

class UrnaUpdate(BaseModel):
    estado: str

# --- Endpoints ---

@app.post(
    "/votos",
    status_code=status.HTTP_201_CREATED,
    summary="Emitir un voto",
    responses={
        201: {"description": "Voto registrado correctamente (voto_confirmado)."},
        400: {"description": "El DNI proporcionado no cumple el formato válido (dni_invalido)."},
        403: {"description": "La urna ya se encuentra cerrada (urna_cerrada)."},
        404: {"description": "El candidato indicado no existe (candidato_inexistente)."},
        409: {"description": "El DNI proporcionado ya ha emitido un voto (dni_ya_registrado)."}
    }
)
async def emitir_voto(voto: VotoCreate):
    global urna_abierta
    
    # 1. Validación de DNI (Regla ABNF: 8 dígitos + 1 letra) -> 400 Bad Request
    if len(voto.dni) != 9 or not voto.dni[:8].isdigit() or not voto.dni[8].isalpha():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="dni_invalido"
        )
    
    # 2. Validación de Candidato -> 404 Not Found
    opcion = voto.candidato.lower()
    if opcion not in opciones_voto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="candidato_inexistente"
        )
        
    async with cerrojo:
        # 3. Validación de estado de urna -> 403 Forbidden
        if not urna_abierta:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="urna_cerrada"
            )
            
        # 4. Validación de Unicidad (Censo) -> 409 Conflict
        if voto.dni in censo_votantes:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="dni_ya_registrado"
            )
            
        # 5. Registro exitoso
        censo_votantes.add(voto.dni)
        opciones_voto[opcion] += 1
        
        return {"mensaje": "voto_confirmado"}

@app.patch(
    "/urna",
    summary="Modificar estado de la urna (Cerrar)",
    responses={
        200: {"description": "Urna cerrada con éxito. Devuelve el recuento y ganadores."},
        400: {"description": "El payload proporcionado es inválido (comando_invalido)."},
        409: {"description": "La urna ya había sido cerrada previamente (urna_ya_cerrada_previamente)."}
    }
)
async def cerrar_urna(urna: UrnaUpdate):
    global urna_abierta
    
    if urna.estado.lower() != "cerrada":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="comando_invalido"
        )
        
    async with cerrojo:
        # Si ya estaba cerrada -> 409 Conflict
        if not urna_abierta:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="urna_ya_cerrada_previamente"
            )
            
        urna_abierta = False
        
        total_votos = sum(opciones_voto.values())
        
        # Caso 1: Urna vacía
        if total_votos == 0:
            return {
                "mensaje": "exito_cierre_vacio",
                "recuento": opciones_voto
            }
            
        # Cálculo de max votos
        max_votos = max(opciones_voto.values())
        ganadores = [k for k, v in opciones_voto.items() if v == max_votos]
        
        # Caso 2: Empate
        if len(ganadores) > 1:
            return {
                "mensaje": "exito_empate",
                "ganadores": ganadores,
                "recuento": opciones_voto
            }
        
        # Caso 3: Ganador único
        return {
            "mensaje": "exito_cierre",
            "ganadores": ganadores,
            "recuento": opciones_voto
        }

@app.get("/urna", summary="Consultar estado de la urna")
async def estado_urna():
    """Endpoint adicional para conocer el estado y resultados si la urna está cerrada."""
    if urna_abierta:
        return {
            "abierta": True,
            "mensaje": "La urna sigue abierta. Resultados ocultos."
        }
    
    return {
        "abierta": False,
        "recuento": opciones_voto
    }

if __name__ == "__main__":
    import uvicorn
    # Se expone a 0.0.0.0 (todas las interfaces) por el punto 5 de la rúbrica
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
