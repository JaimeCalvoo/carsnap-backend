from fastapi import FastAPI, UploadFile, File, HTTPException

from data.cars import cars as CARS_DB
from app.recognition import detect_car_make_model
from app.matching import best_match
from app.rarity import rarity_from_units

app = FastAPI(title="CarSnap Backend", version="0.1")


def format_number_es(n: int) -> str:
    return f"{n:,}".replace(",", ".")


@app.post("/scan")
async def scan_car(image: UploadFile = File(...)):
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Imagen vacía")

    detected = await detect_car_make_model(image_bytes)

    make = detected["make"]
    model = detected["model"]

    key, score = best_match(make, model, CARS_DB)
    if key is None:
        raise HTTPException(status_code=404, detail="No encontrado en base de datos")

    car = CARS_DB[key]
    units = int(car["units_produced"])
    rarity = rarity_from_units(units)

    return {
        "detected": detected,
        "match_score": score,
        "car": {
            "make": car["make"],
            "model": car["model"],
            "price_min": format_number_es(car["price_min_eur"]),
            "price_max": format_number_es(car["price_max_eur"]),
            "units": format_number_es(units),
            "description": car["description"],
            "rarity_percentage": rarity,
        },
    }