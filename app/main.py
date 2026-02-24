from fastapi import FastAPI, UploadFile, File
from app.recognition import detect_car_make_model
from app.matching import best_match
from data.cars import CARS_DB

app = FastAPI(title="CarSnap Backend")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/scan")
async def scan_car(image: UploadFile = File(...)):
    image_bytes = await image.read()

    detected = await detect_car_make_model(image_bytes)
    key, match_score = best_match(detected["make"], detected["model"], CARS_DB)
    car = CARS_DB.get(key)

    return {
        "detected": detected,
        "match_score": match_score,
        "car": car,
    }