from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    predicted_class = db.Column(db.String(100), nullable=False)
