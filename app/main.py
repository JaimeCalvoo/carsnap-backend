from fastapi import FastAPI, UploadFile, File
from app.recognition import detect_car_make_model
from app.matching import find_best_match

app = FastAPI(title="CarSnap Backend")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/scan")
async def scan_car(image: UploadFile = File(...)):
    image_bytes = await image.read()

    detected = await detect_car_make_model(image_bytes)
    car, match_score = find_best_match(detected["make"], detected["model"])

    return {
        "detected": detected,
        "match_score": match_score,
        "car": car,
    }