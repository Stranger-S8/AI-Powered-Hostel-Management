import joblib
import pandas as pd

# Load the model and label encoder
model_pipeline = joblib.load("utils/priority_classifier.pkl")
label_encoder = joblib.load("utils/priority_label_encoder.pkl")

def extract_features(complaint_text, complaint_type):
    # Simple features — replicate your training features
    text_length = len(complaint_text)
    exclamation_count = complaint_text.count("!")
    has_urgent_word = int(any(word in complaint_text.lower() for word in ["urgent", "asap", "immediately", "now"]))
    caps_ratio = sum(1 for c in complaint_text if c.isupper()) / len(complaint_text) if len(complaint_text) > 0 else 0
    sentiment_score = 0  # Optional: If not used, leave as 0 or integrate a library later

    # Build a DataFrame in same format as training
    features = pd.DataFrame([{
        "complaint_text": complaint_text,
        "complaint_type": complaint_type,
        "text_length": text_length,
        "exclamation_count": exclamation_count,
        "has_urgent_word": has_urgent_word,
        "caps_ratio": caps_ratio,
        "sentiment_score": sentiment_score,
    }])

    return features

def predict_priority(features_df):
    prediction_encoded = model_pipeline.predict(features_df)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]
    return prediction_label
