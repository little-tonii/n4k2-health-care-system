import numpy as np
import tensorflow as tf
import json
from typing import List, Dict, Tuple

# Define symptoms and diseases
SYMPTOMS = [
    "Fever", "Cough", "Sore throat", "Fatigue", "Shortness of breath",
    "Chest pain", "Headache", "Runny nose", "Sneezing", "Muscle pain",
    "Joint pain", "Nausea", "Vomiting", "Diarrhea", "Abdominal pain",
    "Weight loss", "Irritability", "Rash", "Swelling", "Anxiety",
    "Depressed mood", "Itching", "Dizziness", "Palpitations", "Blurred vision"
]

DISEASES = [
    "Flu", "Cold", "Sore Throat", "Pneumonia", "Sinusitis",
    "Asthma", "Gastritis", "Peptic Ulcer", "Diabetes", "Hypertension",
    "Coronary Heart Disease", "Stroke", "Hepatitis B", "Hepatitis C",
    "Tuberculosis", "Hypothyroidism", "Anxiety Disorder", "Depression",
    "Eczema", "Gout"
]

# Training data (simplified for web use)
X_train = np.array([
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
], dtype=np.float32)

y_train = tf.keras.utils.to_categorical([i for i in range(len(DISEASES))], num_classes=len(DISEASES))

def build_model() -> tf.keras.Model:
    """Build and compile the disease prediction model."""
    inputs = tf.keras.Input(shape=(len(SYMPTOMS),))
    x = tf.keras.layers.Dense(16, activation='relu')(inputs)
    x = tf.keras.layers.Dropout(0.5)(x, training=True)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x, training=True)
    outputs = tf.keras.layers.Dense(len(DISEASES), activation='softmax')(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Initialize and train the model
model = build_model()
model.fit(X_train, y_train, epochs=100, verbose=0)

def predict_with_uncertainty(model: tf.keras.Model, x: np.ndarray, n_iter: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """Make predictions with uncertainty estimation using Monte Carlo dropout."""
    preds = np.array([model(x, training=True).numpy() for _ in range(n_iter)])
    mean = preds.mean(axis=0)
    std = preds.std(axis=0)
    return mean, std

def get_diagnosis(symptoms: List[str]) -> List[Dict]:
    """
    Get diagnosis based on selected symptoms.
    
    Args:
        symptoms: List of selected symptoms
        
    Returns:
        List of dictionaries containing diagnosis information
    """
    # Convert symptoms to input array
    input_symptoms = [1 if symptom in symptoms else 0 for symptom in SYMPTOMS]
    input_array = np.array([input_symptoms], dtype=np.float32)
    
    # Get predictions
    mean_probs, std_probs = predict_with_uncertainty(model, input_array)
    
    # Get top 3 diagnoses
    top_indices = np.argsort(mean_probs[0])[-3:][::-1]
    diagnoses = []
    
    # Load treatment data
    with open('./chatbot_service/data.json', 'r') as f:
        treatment_data = json.load(f)
    
    # Create diagnosis objects
    for idx in top_indices:
        disease = DISEASES[idx]
        diagnosis = {
            "disease": disease,
            "probability": float(mean_probs[0][idx]),
            "uncertainty": float(std_probs[0][idx])
        }
        
        # Add treatment information
        if disease in treatment_data:
            diagnosis.update(treatment_data[disease])
        
        diagnoses.append(diagnosis)
    
    return diagnoses