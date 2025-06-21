import os
import pickle
import compress_pickle
import gdown
import numpy as np
from flask import Flask, request, render_template

app = Flask(__name__)
model = None

MODEL_PATH = "random_forest_model.gz"

def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Google Drive...")
        gdown.download(GOOGLE_DRIVE_URL, MODEL_PATH, quiet=False)
    model = compress_pickle.load(MODEL_PATH, compression="gzip")

@app.before_request
def initialize():
    global model
    if model is None:
        load_model()

@app.route('/')
def index():
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
        predicted_text = f"₹ {prediction:,.2f}"
        return render_template('index.html', prediction_text=predicted_text)
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
