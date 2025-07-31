import json
import os
from app import app, db, Character, Move

def dash(move_data):
    return {k: (v if v != "" else "-") for k, v in move_data.items()}

def load_character_from_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
        existing_character = Character.query.filter_by(name=data['name']).first()

        if existing_character:
            print(f"Updating character: {data['name']}")
            # Optional: Clear their current moves if you're doing full replacement
            Move.query.filter_by(character_id=existing_character.id).delete()
        else:
            existing_character = Character(name=data['name'])
            db.session.add(existing_character)
            db.session.flush()  # get ID for foreign keys

        # Load moves
        for move_data in data['moves']:
            move_name = move_data.get("name", "")
            # Optional: Skip if move already exists (by name)
            existing_move = Move.query.filter_by(character_id=existing_character.id, name=move_name).first()
            if not existing_move:
                move = Move(character_id=existing_character.id, **dash(move_data))
                db.session.add(move)

with app.app_context():
    db.create_all() # create new database

    data_dir = "data/characters"
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            load_character_from_json(os.path.join(data_dir, filename))

    db.session.commit()