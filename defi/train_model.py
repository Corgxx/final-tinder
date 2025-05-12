
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

def train_model():
    try:
        df = pd.read_csv("user_feedback.csv")
        df["category"] = df["category"].astype("category").cat.codes
        X = df[["category", "rating", "distance"]]
        y = df["match"]

        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump((model, dict(enumerate(df["category"].astype("category").cat.categories))), "model.pkl")
        print("Model trained and saved.")
    except Exception as e:
        print("Training failed:", e)
