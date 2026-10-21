"""
AutoDoc Backend - FastAPI Server
MVP para gestión de fichas de intervención de coches usando archivos locales.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List
import os

app = FastAPI(title="AutoDoc API", version="1.0.0")

# Directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CARS_DIR = DATA_DIR / "cars"
IMAGES_DIR = DATA_DIR / "images"
STATIC_DIR = BASE_DIR / "static"

# Crear directorios si no existen
CARS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


# Modelos Pydantic
class DraftUpdate(BaseModel):
    draft: str


class CarMetadata(BaseModel):
    title: str
    plate: str
    imageURL: Optional[str] = None
    draft: Optional[str] = None
    hasDraft: bool = False


class AIGenerateRequest(BaseModel):
    draft: str


# Funciones auxiliares
def parse_car_file(file_path: Path) -> CarMetadata:
    """Lee y parsea un archivo de coche .txt"""
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    content = file_path.read_text(encoding="utf-8")

    # Parsear cabeceras
    lines = content.split("\n")
    metadata = {}
    draft_started = False
    draft_lines = []

    for line in lines:
        if line.strip() == "---":
            continue

        if draft_started:
            draft_lines.append(line)
        elif line.startswith("Draft:"):
            draft_started = True
            # Incluir el resto de la línea después de "Draft:"
            draft_text = line.replace("Draft:", "").strip()
            if draft_text:
                draft_lines.append(draft_text)
        elif ":" in line and not draft_started:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    draft = "\n".join(draft_lines).strip()

    # Validar campos obligatorios
    if "Title" not in metadata or "Plate" not in metadata:
        raise ValueError("Archivo inválido: faltan campos Title o Plate")

    return CarMetadata(
        title=metadata["Title"],
        plate=metadata["Plate"],
        imageURL=metadata.get("ImageURL", "/data/images/placeholder.jpg"),
        draft=draft if draft else None,
        hasDraft=bool(draft)
    )


def save_car_file(plate: str, car_data: CarMetadata) -> None:
    """Guarda los datos de un coche en su archivo .txt"""
    file_path = CARS_DIR / f"{plate}.txt"

    content = f"""Title: {car_data.title}
Plate: {car_data.plate}
ImageURL: {car_data.imageURL or '/data/images/placeholder.jpg'}
---
Draft:
{car_data.draft or ''}"""

    file_path.write_text(content, encoding="utf-8")


# Endpoints API

@app.get("/api/cars", response_model=List[CarMetadata])
async def list_cars():
    """Lista todos los coches disponibles"""
    cars = []

    for file_path in CARS_DIR.glob("*.txt"):
        try:
            car = parse_car_file(file_path)
            cars.append(car)
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            continue

    return cars


@app.get("/api/cars/{plate}", response_model=CarMetadata)
async def get_car(plate: str):
    """Obtiene los detalles de un coche específico"""
    file_path = CARS_DIR / f"{plate}.txt"

    try:
        car = parse_car_file(file_path)
        return car
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/cars/{plate}/draft")
async def update_draft(plate: str, draft_update: DraftUpdate):
    """Actualiza el borrador de un coche"""
    file_path = CARS_DIR / f"{plate}.txt"

    try:
        # Leer datos actuales
        car = parse_car_file(file_path)

        # Actualizar draft
        car.draft = draft_update.draft
        car.hasDraft = bool(draft_update.draft.strip())

        # Guardar
        save_car_file(plate, car)

        return {"message": "Borrador guardado ✅", "car": car}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando borrador: {str(e)}")


@app.post("/api/cars/import")
async def import_car(file: UploadFile = File(...)):
    """Importa un nuevo coche desde un archivo .txt"""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .txt")

    try:
        # Leer contenido del archivo
        content = await file.read()
        content_str = content.decode("utf-8")

        # Crear archivo temporal para parsear
        temp_path = CARS_DIR / "temp.txt"
        temp_path.write_text(content_str, encoding="utf-8")

        # Parsear y validar
        car = parse_car_file(temp_path)

        # Guardar con el nombre correcto (basado en matrícula)
        final_path = CARS_DIR / f"{car.plate}.txt"
        temp_path.rename(final_path)

        return {"message": f"Coche {car.plate} importado correctamente", "car": car}

    except ValueError as e:
        # Limpiar archivo temporal si existe
        temp_path = CARS_DIR / "temp.txt"
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=400, detail=f"Archivo inválido: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importando coche: {str(e)}")


@app.post("/api/cars/{plate}/generate-description")
async def generate_description(plate: str, request: AIGenerateRequest):
    """
    Genera descripción técnica a partir del borrador usando IA.
    NOTA: Esta funcionalidad debe ser implementada por el alumnado.
    """
    if not request.draft or not request.draft.strip():
        raise HTTPException(status_code=400, detail="El borrador está vacío")

    try:
        # Llamar al servicio de IA (stub - a implementar por alumnado)
        description = generate_description_from_draft(request.draft)

        return {
            "description": description,
            "message": "Descripción generada correctamente"
        }
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Funcionalidad pendiente de implementación. El alumnado debe completar ai_service.py"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando descripción: {str(e)}"
        )


# Servir archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/data/images", StaticFiles(directory=IMAGES_DIR), name="images")


@app.get("/")
async def root():
    """Sirve la página principal"""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servidor funciona"""
    return {
        "status": "ok",
        "cars_count": len(list(CARS_DIR.glob("*.txt"))),
        "data_dir": str(DATA_DIR)
    }


if __name__ == "__main__":
    import uvicorn
    print("🚗 Iniciando servidor AutoDoc en http://localhost:8000")
    print(f"📁 Directorio de datos: {DATA_DIR}")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
