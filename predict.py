
import joblib
import numpy as np

def predict_match_probability(activity):
    try:
        model, cat_map = joblib.load("model.pkl")
        category = activity.get("category", "")
        rating = activity.get("rating", 0)
        distance = activity.get("distance", 0)

        # Encode category
        inv_map = {v: k for k, v in cat_map.items()}
        category_encoded = inv_map.get(category, -1)
        if category_encoded == -1:
            return 0.5

        X = np.array([[category_encoded, rating, distance]])
        prob = model.predict_proba(X)[0][1]
        return prob
    except:
        return 0.5
