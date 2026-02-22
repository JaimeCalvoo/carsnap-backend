from rapidfuzz import fuzz

def best_match(detected_make, detected_model, cars_db):
    detected = f"{detected_make} {detected_model}".lower().strip()
    best_key = None
    best_score = -1

    for key, car in cars_db.items():
        candidate = f"{car['make']} {car['model']}".lower().strip()
        score = fuzz.token_sort_ratio(detected, candidate)
        if score > best_score:
            best_score = score
            best_key = key

    return best_key, best_score