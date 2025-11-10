from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from .database import SessionLocal, engine
from .update_cluster_info import CLUSTER_DEFINITIONS
import joblib
import numpy as np
import pandas as pd
import json
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # Frontend development server
    "http://1227.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load the trained K-Means model
MODEL_PATH = "ml_models/kmeans_model.pkl"
kmeans_model = None
try:
    if os.path.exists(MODEL_PATH):
        kmeans_model = joblib.load(MODEL_PATH)
        print("K-Means model loaded successfully.")
    else:
        print(f"Warning: K-Means model not found at {MODEL_PATH}. Please run train_model.py.")
except Exception as e:
    print(f"Error loading K-Means model: {e}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Game Recommender API!"}

@app.get("/questions/", response_model=list[schemas.Question])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    return questions

@app.post("/recommend/", response_model=schemas.RecommendationResult)
def recommend_games(user_input: schemas.UserResponseInput, db: Session = Depends(get_db)):
    if kmeans_model is None:
        raise HTTPException(status_code=500, detail="K-Means model not loaded.")

    # 1. Preprocess user responses
    response_dict = {res.question_id: res.response_value for res in user_input.responses if res.response_value is not None}
    user_response_vector = np.array([
        response_dict.get(i, 3) for i in range(1, 16) # Default to 3 if not answered
    ]).reshape(1, -1)

    # 2. Predict the cluster
    cluster_id_predicted = int(kmeans_model.predict(user_response_vector)[0]) + 1

    # 3. Retrieve cluster details from the database
    cluster_profile = db.query(models.Cluster).filter(models.Cluster.id == cluster_id_predicted).first()
    if not cluster_profile:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id_predicted} not found.")

    # 4. Get genre recommendations from CLUSTER_DEFINITIONS
    cluster_definition = CLUSTER_DEFINITIONS.get(cluster_id_predicted)
    if not cluster_definition:
        raise HTTPException(status_code=404, detail=f"Recommendation definition for cluster {cluster_id_predicted} not found.")

    recommended_genres = cluster_definition["genres"]
    recommendation_reason = cluster_definition["reason"]

    # 5. Find games matching the recommended genres, prioritizing popular games
    # First, try to get up to 3 popular games
    popular_games = db.query(models.Game).filter(
        models.Game.genre.in_(recommended_genres),
        models.Game.is_popular == True
    ).order_by(func.random()).limit(3).all()

    recommended_games = popular_games
    num_needed = 3 - len(popular_games)

    # If we still need more games, get random non-popular games
    if num_needed > 0:
        # Get IDs of already selected popular games to exclude them
        popular_game_ids = [game.id for game in popular_games]
        
        other_games = db.query(models.Game).filter(
            models.Game.genre.in_(recommended_genres),
            models.Game.id.notin_(popular_game_ids)
        ).order_by(func.random()).limit(num_needed).all()
        recommended_games.extend(other_games)

    return schemas.RecommendationResult(
        profile=schemas.Cluster.from_orm(cluster_profile),
        recommended_games=[schemas.Game.from_orm(game) for game in recommended_games],
        recommendation_reason=recommendation_reason
    )