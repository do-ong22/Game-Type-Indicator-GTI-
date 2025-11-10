from pydantic import BaseModel
from typing import List, Optional

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True

class UserResponseBase(BaseModel):
    question_id: int
    response_value: Optional[int] = None

class UserResponseCreate(UserResponseBase):
    session_id: str

class UserResponse(UserResponseBase):
    id: int
    session_id: str

    class Config:
        from_attributes = True

class UserResponseInput(BaseModel):
    session_id: str
    responses: List[UserResponseBase]

class GameBase(BaseModel):
    freetogame_id: int
    title: str
    thumbnail: Optional[str] = None
    short_description: Optional[str] = None
    game_url: Optional[str] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    publisher: Optional[str] = None
    developer: Optional[str] = None
    release_date: Optional[str] = None
    profile_url: Optional[str] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        from_attributes = True

class ClusterBase(BaseModel):
    name: str
    description: str
    centroid_values: Optional[str] = None # JSON string

class ClusterCreate(ClusterBase):
    pass

class Cluster(ClusterBase):
    id: int

    class Config:
        from_attributes = True

class RecommendationResult(BaseModel):
    profile: Cluster
    recommended_games: List[Game]
    recommendation_reason: str
