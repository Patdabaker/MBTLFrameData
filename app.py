from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    moves = db.relationship('Move', backref='character', lazy=True)

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    input = db.Column(db.String(50))
    damage = db.Column(db.String(50))
    guard = db.Column(db.String(50))
    cancel = db.Column(db.String(50))
    move_property = db.Column(db.String(50))
    cost = db.Column(db.String(50))
    attribute = db.Column(db.String(50))
    startup = db.Column(db.String(50))
    active = db.Column(db.String(50))
    recovery = db.Column(db.String(50))
    overall = db.Column(db.String(50))
    advantage = db.Column(db.String(50))
    invulnerability = db.Column(db.String(50))
    notes = db.Column(db.Text)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/characters')
def character_list():
    characters = Character.query.all()
    return render_template('characters.html', characters=characters)

@app.route('/characters/<int:character_id>')
def character_detail(character_id):
    character = Character.query.get_or_404(character_id)
    return render_template('character_detail.html', character=character)

if __name__ == '__main__':
    app.run(debug=True)