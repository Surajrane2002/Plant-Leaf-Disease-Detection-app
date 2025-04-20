from PIL import Image
import numpy as np
import tensorflow as tf
import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, logging, request, jsonify
from database import get_db_connection
from config import CLASS_LABELS
import logging

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

# ✅ Image Validation (size and aspect ratio check)
def validate_image(img_path):
    try:
        with Image.open(img_path) as img:
            # Check if image is too small
            if img.size[0] < 100 or img.size[1] < 100:
                return False, "Image too small"
            # Check aspect ratio (reasonable for plant images)
            if img.size[0] / img.size[1] < 0.5 or img.size[0] / img.size[1] > 2:
                return False, "Invalid aspect ratio. Please upload a clear plant image."
            return True, None
    except Exception as e:
        return False, f"Error validating image: {str(e)}"

# ✅ Preprocessing function
def preprocess_image(img_path):
    img = Image.open(img_path).resize((128, 128))
    img_array = np.array(img)
    return np.expand_dims(img_array, axis=0)

# ✅ Prediction Route
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

        # Save file securely
        filename = secure_filename(file.filename)
        temp_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{filename}")
        file.save(temp_filename)

        # ✅ Validate Image
        is_valid, error_message = validate_image(temp_filename)
        if not is_valid:
            os.remove(temp_filename)  # Remove invalid image
            return jsonify({"message": f"Invalid image: {error_message}"}), 400

        # ✅ Run Model Prediction
        img_array = preprocess_image(temp_filename)
        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction, axis=1)[0])
        confidence = float(np.max(prediction) * 100)

        # ✅ Get crop and disease name
        label = CLASS_LABELS.get(predicted_class, {"crop": "Unknown", "disease": "Unknown"})
        crop = label["crop"]
        disease = label["disease"]

        # ✅ Save Prediction to Database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO predictions (user_id, image_path, prediction_result, confidence) VALUES (%s, %s, %s, %s)",
            (1, temp_filename, predicted_class, confidence)
        )
        connection.commit()
        cursor.close()
        connection.close()

        # ✅ Optionally delete image after processing
        os.remove(temp_filename)

        # ✅ Return result to the frontend
        return jsonify({
            "crop": crop,
            "disease": disease,
            "confidence": f"{confidence:.2f}"
        }), 200

    except Exception as e:
    # Log the actual error for debugging
     logging.error(f"Prediction error: {str(e)}")

    # Send a friendly error message to frontend
    return jsonify({"message": "Invalid image. Please upload a clear plant leaf image in JPG or PNG format."}), 400
