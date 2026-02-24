from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.recognition import detect_car_from_image_bytes
from app.matching import best_match
from app.rarity import compute_rarity_percentage
from data.cars import cars  # <-- tu diccionario se llama "cars" (según tu captura)

load_dotenv()

app = FastAPI(title="CarSnap Backend", version="1.0")

# CORS (para que luego una web/app móvil pueda llamar a tu API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "CarSnap backend running"}

@app.post("/scan")
async def scan_car(file: UploadFile = File(...)):
    """
    Sube una imagen y devuelve el coche detectado + datos de base.
    IMPORTANTE: el campo se llama 'file' para que Swagger funcione.
    """
    image_bytes = await file.read()

    # 1) Detección (IA o modo gratis)
    detected = await detect_car_from_image_bytes(image_bytes)

    detected_make = detected.get("make")
    detected_model = detected.get("model")
    confidence = detected.get("confidence", None)

    # 2) Matching en tu base de datos local
    key, match_score = best_match(detected_make, detected_model, cars)

    if not key:
        return {
            "detected": detected,
            "match_score": match_score,
            "car": None,
            "error": "No match found in local database"
        }

    car = cars[key].copy()

    # 3) Rareza (si tienes units_produced en tu base)
    units = car.get("units_produced")
    if isinstance(units, int) and units > 0:
        car["rarity_percentage"] = compute_rarity_percentage(units, cars)
    else:
        car["rarity_percentage"] = None

    # 4) Respuesta final
    return {
        "detected": {
            "make": detected_make,
            "model": detected_model,
            "confidence": confidence
        },
        "match_score": match_score,
        "car_key": key,
        "car": car
    }