from transformers import pipeline

print("Loading classification model...")
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)
print("Model loaded successfully.")

CATEGORIES = ["emergency", "routine", "follow-up", "other"]

def classify_text(text: str):
    result = classifier(text, CATEGORIES)
    return result["labels"][0], float(result["scores"][0])
