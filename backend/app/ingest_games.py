import requests
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
from deep_translator import GoogleTranslator
import time

# Set of popular game titles to be flagged
POPULAR_GAMES = {
    "Overwatch 2", "PUBG: BATTLEGROUNDS", "League of Legends", "Apex Legends",
    "Fortnite", "Valorant", "Destiny 2", "Warframe", "Genshin Impact",
    "Lost Ark", "Path of Exile", "Team Fortress 2", "Dota 2", "Rocket League",
    "Brawlhalla", "Smite", "Paladins", "World of Tanks", "World of Warships",
    "Hearthstone: Heroes of Warcraft", "Fall Guys", "Roblox", "Guild Wars 2",
    "Star Wars: The Old Republic", "The Elder Scrolls: Legends"
}

# Drop and recreate tables to apply schema changes
print("Dropping and recreating tables to apply schema changes...")
# Drop recommendations first due to foreign key constraint
models.Recommendation.__table__.drop(engine, checkfirst=True)
models.Game.__table__.drop(engine, checkfirst=True)
models.Base.metadata.create_all(bind=engine)
print("Tables recreated.")

def get_games_from_api():
    """Fetches game data from the FreeToGame API."""
    API_URL = "https://www.freetogame.com/api/games"
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching games from API: {e}")
        return None

def ingest_games_to_db(db: Session, games_data: list):
    """Ingests game data into the database, with translation and popularity flag."""
    if not games_data:
        print("No game data to ingest.")
        return

    print(f"Attempting to ingest {len(games_data)} games with translation and popularity flags...")
    added_count = 0

    for game_data in games_data:
        try:
            existing_game = db.query(models.Game).filter(
                models.Game.freetogame_id == game_data['id']
            ).first()

            if existing_game:
                continue

            original_description = game_data.get('short_description', '')
            translated_description = original_description
            if original_description:
                try:
                    translated_description = GoogleTranslator(source='auto', target='ko').translate(original_description)
                    print(f"Translated '{game_data.get('title')}': {original_description[:30]}... -> {translated_description[:30]}...")
                except Exception as e:
                    print(f"Could not translate description for '{game_data.get('title')}'. Using original. Error: {e}")
                    translated_description = original_description

            is_popular = game_data.get('title') in POPULAR_GAMES

            game = models.Game(
                freetogame_id=game_data.get('id'),
                title=game_data.get('title'),
                thumbnail=game_data.get('thumbnail'),
                short_description=translated_description,
                game_url=game_data.get('game_url'),
                genre=game_data.get('genre'),
                platform=game_data.get('platform'),
                publisher=game_data.get('publisher'),
                developer=game_data.get('developer'),
                release_date=game_data.get('release_date'),
                profile_url=game_data.get('profile_url'),
                is_popular=is_popular
            )
            db.add(game)
            db.commit()
            db.refresh(game)
            added_count += 1
        except IntegrityError:
            db.rollback()
            print(f"Integrity error for game '{game_data.get('title')}' (ID: {game_data.get('id')}). Rolling back.")
        except Exception as e:
            db.rollback()
            print(f"Error ingesting game '{game_data.get('title')}' (ID: {game_data.get('id')}): {e}")
    print(f"Successfully ingested {added_count} new games.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Fetching games from API and ingesting into database...")
        games = get_games_from_api()
        if games:
            ingest_games_to_db(db, games)
    finally:
        db.close()
