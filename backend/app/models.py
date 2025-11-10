from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base, engine, SessionLocal # Import from database.py

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    # We can add a 'theme' or 'dimension' column later if needed for more structured analysis
    # theme = Column(String, index=True)

    def __repr__(self):
        return f"<Question(id={self.id}, text='{self.text[:30]}...')>"

class UserResponse(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False) # To group responses from one user session
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    response_value = Column(Integer, nullable=False) # 1-5 for Likert scale

    question = relationship("Question")

    def __repr__(self):
        return f"<UserResponse(id={self.id}, session_id='{self.session_id}', question_id={self.question_id}, response_value={self.response_value})>"

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    freetogame_id = Column(Integer, unique=True, nullable=False) # ID from FreeToGame API
    title = Column(String, nullable=False)
    thumbnail = Column(String)
    short_description = Column(Text)
    game_url = Column(String)
    genre = Column(String)
    platform = Column(String)
    publisher = Column(String)
    developer = Column(String)
    release_date = Column(String) # Store as string for simplicity, can convert to Date later
    profile_url = Column(String)
    is_popular = Column(Boolean, default=False, nullable=False)
    # We can add a 'tags' column later if the API provides it as a list/JSON

    def __repr__(self):
        return f"<Game(id={self.id}, title='{self.title}', genre='{self.genre}')>"

class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # e.g., "The Strategic Planner"
    description = Column(Text, nullable=False)
    # Store the centroid values for each cluster for visualization/comparison
    centroid_values = Column(Text) # Store as JSON string or similar

    def __repr__(self):
        return f"<Cluster(id={self.id}, name='{self.name}')>"

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    reason = Column(Text, nullable=False) # Why this game is recommended for this cluster

    cluster = relationship("Cluster")
    game = relationship("Game")

    def __repr__(self):
        return f"<Recommendation(id={self.id}, cluster_id={self.cluster_id}, game_id={self.game_id})>"

# Function to create tables
def create_db_tables():
    Base.metadata.create_all(bind=engine)

# Example usage (for testing connection and table creation)
if __name__ == "__main__":
    # IMPORTANT: Replace with your actual PostgreSQL connection string
    # For local testing, you might use a SQLite in-memory database:
    # DATABASE_URL = "sqlite:///:memory:"
    # engine = create_engine(DATABASE_URL)
    # Base.metadata.create_all(bind=engine)
    # print("Tables created successfully (in-memory SQLite for example).")
    
    # For actual PostgreSQL, ensure your DATABASE_URL is correct
    # and PostgreSQL server is running.
    print("Attempting to create tables in PostgreSQL...")
    create_db_tables()
    print("Tables creation attempt finished. Check your database.")
