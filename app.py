# app.py
from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import gzip
import gdown
import os

app = Flask(__name__)

model_path = "random_forest_model.pkl"
gdrive_file_id = "1HTDE28HhFk47wnIiePTp4Ebr9NJ60DG0"  # 👈 Replace with your actual file ID

if not os.path.exists(model_path):
    print("Downloading model from Google Drive...")
    url = f"https://drive.google.com/uc?id={gdrive_file_id}"
    gdown.download(url, model_path, quiet=False)

# Load the trained model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [
            float(request.form.get('bedrooms', 0)),
            float(request.form.get('bathrooms', 0)),
            float(request.form.get('living_area', 0)),
            float(request.form.get('lot_area', 0)),
            float(request.form.get('number_of_floors', 0)),
            float(request.form.get('waterfront_present', 0)),
            float(request.form.get('number_of_views', 0)),
            float(request.form.get('grade_of_the_house', 0)),
            float(request.form.get('area_of_basement', 0)),
            float(request.form.get('postal_code', 0)),
            float(request.form.get('lattitude', 0)),
            float(request.form.get('living_area_renov', 0)),
            float(request.form.get('lot_area_renov', 0)),
            float(request.form.get('renovation_age', 0))
        ]

        final_input = np.array([features])
        prediction = model.predict(final_input)[0]
        predicted_price = f"₹ {prediction:,.2f}"

        return render_template('index.html', prediction_text=predicted_text)
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
