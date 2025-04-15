from flask import Blueprint, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os
import uuid
from werkzeug.utils import secure_filename
from database import get_db_connection
from config import CLASS_LABELS

predict_blueprint = Blueprint("predict", __name__)

# ✅ Model and upload path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model_checkpoint.keras")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Load model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# ✅ Preprocess function
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    return np.expand_dims(img_array, axis=0)


# ✅ PREDICTION ROUTE
@predict_blueprint.route("/api/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"message": "Model not loaded"}), 500

        if "image" not in request.files:
            return jsonify({"message": "No image uploaded"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"message": "Empty filename"}), 400

        # ✅ Save file securely
        filename = secure_filename(file.filename)
        temp_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{filename}")
        file.save(temp_filename)

        # ✅ Run model prediction
        img_array = preprocess_image(temp_filename)
        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction, axis=1)[0])
        confidence = float(np.max(prediction) * 100)

        # ✅ Get crop and disease name
        label = CLASS_LABELS.get(predicted_class, {"crop": "Unknown", "disease": "Unknown"})
        crop = label["crop"]
        disease = label["disease"]

        # ✅ Save to database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO predictions (user_id, image_path, prediction_result, confidence) VALUES (%s, %s, %s, %s)",
            (1, temp_filename, predicted_class, confidence)
        )
        connection.commit()
        cursor.close()
        connection.close()

        # ✅ Optionally delete image
        os.remove(temp_filename)

        # ✅ Return result in frontend-friendly format
        return jsonify({
            "crop": crop,
            "disease": disease,
            "confidence": f"{confidence:.2f}"
        }), 200

    except Exception as e:
        return jsonify({"message": f"Prediction error: {str(e)}"}), 500
