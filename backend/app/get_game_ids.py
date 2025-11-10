import json
from app.database import SessionLocal
from app.models import Game

db = SessionLocal()
try:
    game_titles = [
        'Overwatch 2', 'PUBG: BATTLEGROUNDS', 'Game Of Thrones Winter Is Coming',
        'Elvenar', 'Throne And Liberty', 'Neverwinter', 'Lost Ark',
        # Add other games that might be good recommendations, even if not in sample
        'Minecraft', 'Stardew Valley', 'League of Legends', 'Civilization VI', 'Hades'
    ]
    
    # Fetch all games first, then filter in Python to handle potential case differences or partial matches
    all_games = db.query(Game).all()
    
    recommended_games_ids = {}
    for title in game_titles:
        found_game = next((g for g in all_games if title.lower() in g.title.lower()), None)
        if found_game:
            recommended_games_ids[found_game.title] = found_game.id
        else:
            print(f"Warning: Game '{title}' not found in database.")

    print('Recommended Games IDs:')
    for title, game_id in recommended_games_ids.items():
        print(f'- {title}: {game_id}')
finally:
    db.close()
