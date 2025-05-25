import numpy as np
import tensorflow as tf
import pyttsx3
import matplotlib.pyplot as plt
import json

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

diseases = [
  "Flu",
  "Cold",
  "Sore Throat",
  "Pneumonia",
  "Sinusitis",
  "Asthma",
  "Gastritis",
  "Peptic Ulcer",
  "Diabetes",
  "Hypertension",
  "Coronary Heart Disease",
  "Stroke",
  "Hepatitis B",
  "Hepatitis C",
  "Tuberculosis",
  "Hypothyroidism",
  "Anxiety Disorder",
  "Depression",
  "Eczema",
  "Gout"
]

y_train = tf.keras.utils.to_categorical([i for i in range(len(diseases))], num_classes=len(diseases)) # pyright: ignore[reportAttributeAccessIssue]

def build_model():
    inputs = tf.keras.Input(shape=(25,)) # pyright: ignore[reportAttributeAccessIssue]
    x = tf.keras.layers.Dense(16, activation='relu')(inputs) # pyright: ignore[reportAttributeAccessIssue]
    x = tf.keras.layers.Dropout(0.5)(x, training=True) # pyright: ignore[reportAttributeAccessIssue]
    x = tf.keras.layers.Dense(16, activation='relu')(x) # pyright: ignore[reportAttributeAccessIssue]
    x = tf.keras.layers.Dropout(0.5)(x, training=True) # pyright: ignore[reportAttributeAccessIssue]
    outputs = tf.keras.layers.Dense(len(diseases), activation='softmax')(x) # pyright: ignore[reportAttributeAccessIssue]
    return tf.keras.Model(inputs, outputs) # pyright: ignore[reportAttributeAccessIssue]

model = build_model()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, verbose=0)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def predict_with_uncertainty(model, x, n_iter=100):
    preds = np.array([model(x, training=True).numpy() for _ in range(n_iter)])
    mean = preds.mean(axis=0)
    std = preds.std(axis=0)
    return mean, std

def run_virtual_robot():
    print("👋 Hello! I am your virtual health assistant robot.")
    print("Please answer the following questions with Y/N:")
    symptom_names = [
  "Fever", "Cough", "Sore throat", "Fatigue", "Shortness of breath",
  "Chest pain", "Headache", "Runny nose", "Sneezing", "Muscle pain",
  "Joint pain", "Nausea", "Vomiting", "Diarrhea", "Abdominal pain",
  "Weight loss", "Irritability", "Rash", "Swelling", "Anxiety",
  "Depressed mood", "Itching", "Dizziness", "Palpitations", "Blurred vision"
]
    input_symptoms = []
    for name in symptom_names:
        ans = input(f"Do you have {name}? (Y/N): ").strip().lower()
        input_symptoms.append(1 if ans == 'y' else 0)
    input_array = np.array([input_symptoms], dtype=np.float32)
    mean_probs, std_probs = predict_with_uncertainty(model, input_array)
    most_likely = np.argmax(mean_probs)
    diagnosis = diseases[most_likely]
    print("\n🧠 Diagnosis with Probabilities and Uncertainty:")
    for i, dis in enumerate(diseases):
        print(f"{dis}: P={mean_probs[0][i]:.3f}, Uncertainty={std_probs[0][i]:.3f}")
    speak(f"You may have {diagnosis}.")
    print(f"\n🤖 Diagnosis: {diagnosis} (±{std_probs[0][most_likely]:.3f})")

    with open('./data.json', 'r') as f:
        data = json.load(f)
    dis = data[diagnosis]
    treatment = dis['Treatment']
    surgeon = dis['Surgeon']
    medicine = dis['Medicine']
    speak(f'This Diagnosis can be treat such as {treatment} And you shoud {surgeon}. You shoud buy medicine like {medicine}')

    plt.figure(figsize=(12, 6))
    plt.bar(diseases, mean_probs[0], yerr=std_probs[0], capsize=len(diseases), color='skyblue')
    plt.ylabel("Probability")
    plt.title("Diagnosis Confidence")
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.show()

run_virtual_robot()
