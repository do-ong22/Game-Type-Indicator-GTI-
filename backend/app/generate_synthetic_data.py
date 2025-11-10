import numpy as np
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal
import uuid

# Define the 15 questions (as discussed)
QUESTIONS_TEXT = [
    "나는 중요한 결정을 내릴 때 충분한 정보를 수집하고 신중하게 분석하는 편이다.",
    "나는 예상치 못한 상황에 직면했을 때 빠르게 판단하고 즉시 행동하는 것을 선호한다.",
    "나는 복잡한 문제에 부딪혔을 때 포기하지 않고 끈기 있게 해결책을 찾아낸다.",
    "나는 혼자서 목표를 달성하는 것보다 다른 사람들과 협력하여 성과를 내는 것을 선호한다.",
    "나는 팀 프로젝트에서 리더 역할을 맡아 전체를 조율하는 것에 흥미를 느낀다.",
    "나는 개인적인 공간에서 방해받지 않고 집중하여 작업할 때 가장 효율적이다.",
    "나는 새로운 도전과 위험을 감수하면서 성장하는 것을 두려워하지 않는다.",
    "나는 예측 가능하고 안정적인 환경에서 일할 때 편안함을 느낀다.",
    "나는 목표 달성을 위해 경쟁하는 상황에서 더 큰 동기 부여를 얻는다.",
    "나는 작은 부분까지 꼼꼼하게 신경 쓰고 완벽을 추구하는 편이다.",
    "나는 전체적인 흐름과 큰 그림을 파악하는 데 더 집중한다.",
    "나는 여러 가지 일을 동시에 처리하기보다 한 가지 일에 깊이 몰입하는 것을 선호한다.",
    "나는 새로운 지식이나 기술을 배우고 탐구하는 과정 자체를 즐긴다.",
    "나는 정답이 없는 문제에 대해 다양한 가능성을 열어두고 탐색하는 것을 좋아한다.",
    "나는 이미 익숙한 분야에서 전문성을 발휘하고 숙련도를 높이는 것을 선호한다.",
]

# Define archetypal profiles (mean response values for 15 questions, 1-5 scale)
# These are example archetypes based on our 5 dimensions (3 questions per dimension)
# The values are just illustrative and can be refined.
ARCHETYPES = {
    "Strategic Planner": {
        "means": [5, 2, 4,  # Decision-Making (High analysis, low quick, high persistence)
                  3, 4, 2,  # Interaction (Moderate collab, high leadership, low solo)
                  3, 4, 2,  # Challenge (Moderate risk, high stability, low competition)
                  5, 2, 4,  # Detail (High detail, low big picture, high focus)
                  4, 3, 3], # Learning (High new knowledge, moderate exploration, moderate mastery)
        "std_dev": 0.8,
        "num_users": 100
    },
    "Action-Oriented Leader": {
        "means": [3, 5, 4,  # Decision-Making (Moderate analysis, high quick, high persistence)
                  4, 5, 1,  # Interaction (High collab, high leadership, very low solo)
                  5, 2, 5,  # Challenge (High risk, low stability, high competition)
                  2, 4, 3,  # Detail (Low detail, high big picture, moderate focus)
                  3, 4, 2], # Learning (Moderate new knowledge, high exploration, low mastery)
        "std_dev": 0.8,
        "num_users": 100
    },
    "Collaborative Explorer": {
        "means": [3, 3, 3,  # Decision-Making (Moderate on all)
                  5, 3, 3,  # Interaction (High collab, moderate leadership, moderate solo)
                  4, 3, 3,  # Challenge (Moderate risk, moderate stability, moderate competition)
                  3, 4, 2,  # Detail (Moderate detail, high big picture, low focus)
                  5, 5, 1], # Learning (High new knowledge, high exploration, very low mastery)
        "std_dev": 0.8,
        "num_users": 100
    },
    "Detail-Oriented Specialist": {
        "means": [4, 2, 5,  # Decision-Making (High analysis, low quick, high persistence)
                  2, 2, 5,  # Interaction (Low collab, low leadership, high solo)
                  2, 5, 1,  # Challenge (Low risk, high stability, low competition)
                  5, 1, 5,  # Detail (High detail, very low big picture, high focus)
                  4, 2, 5], # Learning (High new knowledge, low exploration, high mastery)
        "std_dev": 0.8,
        "num_users": 100
    }
}

def generate_responses(archetype_name, archetype_data):
    """Generates synthetic responses for a given archetype."""
    responses = []
    for _ in range(archetype_data["num_users"]):
        user_responses = []
        for i in range(15): # 15 questions
            mean = archetype_data["means"][i]
            std_dev = archetype_data["std_dev"]
            # Generate response with noise, clip to 1-5 range
            response_value = int(np.round(np.random.normal(mean, std_dev)))
            response_value = max(1, min(5, response_value))
            user_responses.append(response_value)
        responses.append(user_responses)
    return responses

def store_questions_in_db(db: Session):
    """Stores the predefined questions in the database if they don't exist."""
    for i, text in enumerate(QUESTIONS_TEXT):
        existing_question = db.query(models.Question).filter(models.Question.id == (i + 1)).first()
        if not existing_question:
            question = models.Question(id=(i + 1), text=text)
            db.add(question)
            print(f"Added question: {text[:30]}...")
    db.commit()

def store_synthetic_data_in_db(db: Session):
    """Generates and stores synthetic user responses in the database."""
    store_questions_in_db(db) # Ensure questions are in DB first

    total_responses_added = 0
    for archetype_name, archetype_data in ARCHETYPES.items():
        print(f"Generating data for archetype: {archetype_name}")
        synthetic_responses = generate_responses(archetype_name, archetype_data)
        
        for user_response_set in synthetic_responses:
            session_id = str(uuid.uuid4()) # Unique session ID for each synthetic user
            for i, response_value in enumerate(user_response_set):
                user_response = models.UserResponse(
                    session_id=session_id,
                    question_id=(i + 1), # Assuming question IDs start from 1
                    response_value=response_value
                )
                db.add(user_response)
            total_responses_added += 15 # 15 responses per user
        db.commit()
    print(f"Successfully generated and stored {total_responses_added} synthetic user responses.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        store_synthetic_data_in_db(db)
    finally:
        db.close()
