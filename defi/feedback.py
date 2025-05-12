
import csv
import os

def save_feedback(activity, liked):
    row = {
        "category": activity.get("category", ""),
        "rating": activity.get("rating", 0),
        "distance": activity.get("distance", 0),
        "match": int(liked)
    }

    file_exists = os.path.isfile("user_feedback.csv")
    with open("user_feedback.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
