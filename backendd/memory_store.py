import json
import os

FILE = "user_data/performance.json"


def save_performance(topic, correct):
    data = {}

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            data = json.load(f)

    if topic not in data:
        data[topic] = {"correct": 0, "wrong": 0}

    if correct:
        data[topic]["correct"] += 1
    else:
        data[topic]["wrong"] += 1

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_weak_topics():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        data = json.load(f)

    return [t for t in data if data[t]["wrong"] > data[t]["correct"]]