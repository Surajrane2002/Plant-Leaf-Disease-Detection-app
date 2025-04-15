# config.py

import mysql.connector

# MySQL Configuration
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "plant_disease_db"
MYSQL_PORT = 3306

# Class Labels for Predictions
CLASS_LABELS = {
    0: {"crop": "Apple", "disease": "Apple Scab"},
    1: {"crop": "Apple", "disease": "Black Rot"},
    2: {"crop": "Apple", "disease": "Cedar Apple Rust"},
    3: {"crop": "Apple", "disease": "Healthy"},
    4: {"crop": "Blueberry", "disease": "Healthy"},
    5: {"crop": "Cherry", "disease": "Healthy"},
    6: {"crop": "Cherry", "disease": "Powdery Mildew"},
    7: {"crop": "Corn", "disease": "Cercospora Leaf Spot"},
    8: {"crop": "Corn", "disease": "Common Rust"},
    9: {"crop": "Corn", "disease": "Healthy"},
    10: {"crop": "Corn", "disease": "Northern Leaf Blight"},
    11: {"crop": "Grape", "disease": "Black Rot"},
    12: {"crop": "Grape", "disease": "Esca (Black Measles)"},
    13: {"crop": "Grape", "disease": "Healthy"},
    14: {"crop": "Grape", "disease": "Leaf Blight (Isariopsis Leaf Spot)"},
    15: {"crop": "Orange", "disease": "Haunglongbing (Citrus Greening)"},
    16: {"crop": "Peach", "disease": "Bacterial Spot"},
    17: {"crop": "Peach", "disease": "Healthy"},
    18: {"crop": "Pepper", "disease": "Bell Bacterial Spot"},
    19: {"crop": "Pepper", "disease": "Healthy"},
    20: {"crop": "Potato", "disease": "Early Blight"},
    21: {"crop": "Potato", "disease": "Healthy"},
    22: {"crop": "Potato", "disease": "Late Blight"},
    23: {"crop": "Raspberry", "disease": "Healthy"},
    24: {"crop": "Soybean", "disease": "Healthy"},
    25: {"crop": "Squash", "disease": "Powdery Mildew"},
    26: {"crop": "Strawberry", "disease": "Healthy"},
    27: {"crop": "Strawberry", "disease": "Leaf Scorch"},
    28: {"crop": "Tomato", "disease": "Bacterial Spot"},
    29: {"crop": "Tomato", "disease": "Early Blight"},
    30: {"crop": "Tomato", "disease": "Healthy"},
    31: {"crop": "Tomato", "disease": "Late Blight"},
    32: {"crop": "Tomato", "disease": "Leaf Mold"},
    33: {"crop": "Tomato", "disease": "Septoria Leaf Spot"},
    34: {"crop": "Tomato", "disease": "Spider Mites (Two-Spotted Spider Mite)"},
    35: {"crop": "Tomato", "disease": "Target Spot"},
    36: {"crop": "Tomato", "disease": "Tomato Mosaic Virus"},
    37: {"crop": "Tomato", "disease": "Tomato Yellow Leaf Curl Virus"},
    
    
}
