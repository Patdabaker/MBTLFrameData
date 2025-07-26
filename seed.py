import json
import os
from app import app, db, Character, Move

def dash(move_data):
    return {k: (v if v != "" else "-") for k, v in move_data.items()}

def load_character_from_json(path):
    with open(path, 'r') as file:
        data = json.load(file)

        # Check if character already exists
        existing_character = Character.query.filter_by(name=data['name']).first()
        if existing_character:
            print(f"Character '{data['name']}' already exists. Skipping.")
            return

        character = Character(name=data['name'])
        db.session.add(character)
        db.session.flush()
        for move_data in data['moves']:
            move = Move(character_id=character.id, **dash(move_data))
            db.session.add(move)

with app.app_context():
    db.create_all() # create new database

    data_dir = "data/characters"
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            load_character_from_json(os.path.join(data_dir, filename))

    db.session.commit()