import pandas as pd
from sklearn.cluster import KMeans
import joblib
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal
import json

# Number of clusters (k) - based on our archetypes
NUM_CLUSTERS = 8
MODEL_PATH = "ml_models/kmeans_model.pkl"

def train_and_save_kmeans_model(db: Session):
    """
    Loads synthetic user responses, trains a K-Means model,
    saves the model, and stores cluster info in the database.
    """
    # 1. Load all synthetic user responses from the database
    user_responses_data = db.query(models.UserResponse).all()
    
    if not user_responses_data:
        print("No user response data found in the database. Please generate synthetic data first.")
        return

    # Convert to DataFrame for easier processing
    df_responses = pd.DataFrame([
        {"session_id": r.session_id, "question_id": r.question_id, "response_value": r.response_value}
        for r in user_responses_data
    ])

    # Pivot the table to get user_id as index, question_id as columns, and response_value as values
    # Each row will represent a user's responses to all 15 questions
    user_response_matrix = df_responses.pivot_table(
        index='session_id', columns='question_id', values='response_value'
    ).fillna(0) # Fill any missing responses with 0 (though our synthetic data should be complete)

    # Ensure all 15 questions are present as columns
    for i in range(1, 16):
        if i not in user_response_matrix.columns:
            user_response_matrix[i] = 0
    user_response_matrix = user_response_matrix.reindex(sorted(user_response_matrix.columns), axis=1)


    print(f"Training K-Means model with {len(user_response_matrix)} users and {NUM_CLUSTERS} clusters...")
    
    # 3. Initialize and train a K-Means model
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42, n_init=10)
    kmeans.fit(user_response_matrix)

    # 4. Save the trained K-Means model to a .pkl file
    import os
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(kmeans, MODEL_PATH)
    print(f"K-Means model saved to {MODEL_PATH}")

    # 5. Store the cluster centroids and other relevant information in the 'clusters' table
    # Clear existing recommendations and clusters first to avoid foreign key constraints
    db.query(models.Recommendation).delete()
    db.query(models.Cluster).delete()
    db.commit()

    for i in range(NUM_CLUSTERS):
        centroid = kmeans.cluster_centers_[i].tolist()
        # For PoC, we'll use generic names. These will be manually updated later.
        cluster_name = f"Cluster {i+1}"
        cluster_description = f"This is a generic description for Cluster {i+1}. Please update manually."
        
        cluster = models.Cluster(
            id=i+1, # Explicitly set the ID
            name=cluster_name,
            description=cluster_description,
            centroid_values=json.dumps(centroid) # Store centroid as JSON string
        )
        db.add(cluster)
    db.commit()
    print(f"Stored {NUM_CLUSTERS} cluster centroids and info in the database.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        train_and_save_kmeans_model(db)
    finally:
        db.close()
