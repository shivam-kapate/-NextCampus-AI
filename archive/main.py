from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="MHT-CET Engineering Admission Predictor")

# Global variables for model and encoders
knn_model = None
branch_encoder = None
gender_encoder = None
category_encoder = None

@app.on_event("startup")
def load_assets():
    global knn_model, branch_encoder, gender_encoder, category_encoder
    print("Loading model and encoders...")
    try:
        knn_model = joblib.load('knn_model.joblib')
        branch_encoder = joblib.load('branch_encoder.joblib')
        gender_encoder = joblib.load('gender_encoder.joblib')
        category_encoder = joblib.load('category_encoder.joblib')
        print("Assets loaded successfully.")
    except Exception as e:
        print(f"Error loading assets. Did you run train_model.py? Details: {e}")

# Pydantic schema for the incoming request
class PredictRequest(BaseModel):
    percentile: float
    branch: str
    gender: str
    category: str

@app.post("/predict")
def predict(request: PredictRequest):
    if not all([knn_model, branch_encoder, gender_encoder, category_encoder]):
        raise HTTPException(status_code=500, detail="Model assets not loaded properly. Please train the model first.")

    try:
        # Transform inputs (Handle potential unseen labels by catching ValueError)
        branch_encoded = branch_encoder.transform([request.branch])[0]
        gender_encoded = gender_encoder.transform([request.gender])[0]
        category_encoded = category_encoder.transform([request.category])[0]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input category: {e}")

    # Prepare input array
    input_data = np.array([[request.percentile, branch_encoded, gender_encoded, category_encoded]])

    try:
        # Use kneighbors to find the 5 nearest data points
        distances, indices = knn_model.kneighbors(input_data, n_neighbors=5)
        
        # knn_model._y contains the integer-encoded labels of the training set
        neighbor_class_indices = knn_model._y[indices[0]]
        
        # Map integer-encoded labels back to original college names
        neighbor_colleges = knn_model.classes_[neighbor_class_indices]
        
        # Get the unique top colleges while maintaining distance order (closest first)
        top_colleges = []
        for college in neighbor_colleges:
            if college not in top_colleges:
                top_colleges.append(college)
            if len(top_colleges) == 3:  # Return Top 3 unique colleges
                break
                
        return {"predictions": top_colleges}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serves the frontend index.html"""
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            return f.read()
    return "<h1>Error: index.html not found!</h1>"
