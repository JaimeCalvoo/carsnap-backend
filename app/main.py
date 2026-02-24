from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.recognition import detect_car_from_image_bytes
from app.matching import best_match
from app.rarity import compute_rarity

from data.cars import cars  # <-- IMPORTANTE: aquí está tu BD (variable "cars")

app = FastAPI(title="CarSnap Backend")

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
async def scan_car(image: UploadFile = File(...)):
    image_bytes = await image.read()

    detected = await detect_car_from_image_bytes(image_bytes)
    # detected debe ser algo tipo: {"make": "...", "model": "...", "confidence": 0.xx}

    key, match_score = best_match(detected["make"], detected["model"], cars)

    car_info = None
    if key is not None and key in cars:
        car_info = cars[key].copy()

    rarity_percentage = None
    if car_info:
        rarity_percentage = compute_rarity(car_info)

    return {
        "detected": detected,
        "match_score": match_score,
        "car": car_info,
        "rarity_percentage": rarity_percentage,
    }