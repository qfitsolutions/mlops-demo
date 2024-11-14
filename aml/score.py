import json
import joblib
from azureml.core.model import Model
from flask import Flask, request, jsonify

def init():
    global model
    # Load the model from the registered file
    model_path = Model.get_model_path('iris-classifier')
    model = joblib.load(model_path)

def run(raw_data):
    data = json.loads(raw_data)
    prediction = model.predict([data['data']])
    return json.dumps({'prediction': int(prediction[0])})