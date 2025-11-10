from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal

# --- Cluster Definitions ---
# We now have 8 archetypes. The recommendation logic will be based on genres.
# The 'reason' explains why the genres are a good fit for the archetype.
CLUSTER_DEFINITIONS = {
    1: {
        "name": "도전적인 리더 (Challenging Leader)",
        "description": "빠르게 판단하고 끈기 있게 문제를 해결하며, 강력한 리더십으로 협력을 이끌고 도전과 경쟁을 즐기며 큰 그림을 보는 유형입니다.",
        "genres": ["Shooter", "MOBA", "Strategy"],
        "reason": "빠른 판단력과 리더십을 발휘할 수 있는 경쟁적인 장르가 잘 맞습니다. 팀을 이끌고 전략을 세워 승리하는 경험을 즐길 수 있습니다."
    },
    2: {
        "name": "신중한 분석가 (Prudent Analyst)",
        "description": "신중하게 분석하고 끈기 있게 문제를 해결하며, 안정적인 환경에서 꼼꼼하게 완벽을 추구하고 한 가지 일에 깊이 몰입하는 유형입니다.",
        "genres": ["Strategy", "Card Game", "MMORPG"],
        "reason": "복잡한 시스템을 분석하고 장기적인 계획을 세우는 것을 즐깁니다. 세밀한 자원 관리와 깊이 있는 전략이 요구되는 게임에서 두각을 나타낼 수 있습니다."
    },
    3: {
        "name": "전문적인 장인 (Expert Craftsman)",
        "description": "신중하고 끈기 있게 문제를 해결하며, 개인적인 공간에서 안정적으로 꼼꼼하게 완벽을 추구하고 한 가지 일에 깊이 몰입하여 익숙한 분야의 전문성을 높이는 유형입니다.",
        "genres": ["MMORPG", "ARPG", "Action RPG"],
        "reason": "하나의 캐릭터나 기술을 깊이 파고들어 마스터하는 것을 선호합니다. 아이템 제작, 자원 채집 등 특정 분야의 전문성을 높이는 데서 큰 만족을 느낍니다."
    },
    4: {
        "name": "협력적 탐험가 (Collaborative Explorer)",
        "description": "협력을 매우 선호하고 새로운 도전을 즐기며, 큰 그림을 보고 새로운 지식과 정답 없는 문제를 탐색하는 데 열정적인 유형입니다.",
        "genres": ["MMORPG", "Social", "Co-Op"],
        "reason": "다른 플레이어들과 함께 광활한 세계를 탐험하고 새로운 모험을 떠나는 것을 즐깁니다. 협력을 통해 공동의 목표를 달성하는 데서 기쁨을 느낍니다."
    },
    5: {
        "name": "창의적인 전략가 (Creative Strategist)",
        "description": "혁신적이고 틀에 얽매이지 않는 사고를 하며, 복잡한 시스템 속에서 자신만의 독창적인 해결책을 찾는 것을 즐기는 유형입니다.",
        "genres": ["Strategy", "Sandbox", "Building"],
        "reason": "정해진 규칙을 넘어 자신만의 창의적인 전략을 시험해볼 수 있는 게임이 잘 어울립니다. 복잡한 시스템을 자신만의 방식으로 해석하고 활용하는 데 능숙합니다."
    },
    6: {
        "name": "자유로운 해결사 (Independent Problem-Solver)",
        "description": "자율성을 중시하며, 누구의 도움 없이도 스스로 정보를 찾고 문제를 해결하는 과정에서 만족을 느끼는 독립적인 유형입니다.",
        "genres": ["ARPG", "Action RPG", "Fighting"],
        "reason": "다른 사람에게 의존하지 않고 자신의 실력과 판단만으로 어려움을 극복하는 게임을 선호합니다. 솔로 플레이가 강조되는 게임에서 큰 성취감을 느낄 수 있습니다."
    },
    7: {
        "name": "사교적인 중재자 (Social Mediator)",
        "description": "사람들과의 교류를 중요하게 생각하며, 경쟁보다는 소통과 화합을 통해 긍정적인 관계를 형성하는 것을 즐기는 유형입니다.",
        "genres": ["Social", "MMORPG", "Co-Op"],
        "reason": "다른 플레이어들과 소통하고 커뮤니티를 형성하는 재미를 느낄 수 있는 게임이 잘 맞습니다. 경쟁보다는 협력과 사교 활동에 중점을 둔 게임을 즐깁니다."
    },
    8: {
        "name": "안정적인 실행가 (Steady Executor)",
        "description": "명확한 목표와 절차를 선호하며, 꾸준하고 성실하게 과업을 수행하여 안정적으로 성장하는 과정에서 만족을 느끼는 유형입니다.",
        "genres": ["Strategy", "MMORPG", "Card Game"],
        "reason": "규칙적으로 일일 퀘스트를 수행하거나 자원을 관리하며 꾸준히 성장하는 게임을 즐깁니다. 예측 가능하고 안정적인 환경에서 성실하게 목표를 달성하는 데서 재미를 느낍니다."
    }
}

def update_cluster_info(db: Session):
    """
    Updates cluster names and descriptions in the database.
    Recommendation logic is now handled in the main application logic, not here.
    """
    print("Updating cluster names and descriptions...")

    for cluster_id, cluster_data in CLUSTER_DEFINITIONS.items():
        cluster = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
        if cluster:
            cluster.name = cluster_data["name"]
            cluster.description = cluster_data["description"]
            db.add(cluster)
            print(f"Updated Cluster {cluster_id}: {cluster.name}")
        else:
            print(f"Warning: Cluster with ID {cluster_id} not found. It should have been created by train_model.py.")
            continue

    db.commit()
    print("Cluster information updated successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        update_cluster_info(db)
    finally:
        db.close()
