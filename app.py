# app.py
from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import gzip
app = Flask(__name__)

# Load the trained model
with gzip.open('random_forest_model.pkl.gz', 'rb') as file:
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

        return render_template("result.html", prediction_text=predicted_price)
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
