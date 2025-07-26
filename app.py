from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'patdabaker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class GeneralNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opponent_character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    opponent_character = db.relationship('Character', foreign_keys=[opponent_character_id])

class MatchupNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    my_character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    opponent_character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    my_character = db.relationship('Character', foreign_keys=[my_character_id])
    opponent_character = db.relationship('Character', foreign_keys=[opponent_character_id])

class MoveMatchupNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    move_id = db.Column(db.Integer, db.ForeignKey('move.id'), nullable=False)
    my_character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    opponent_character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    content = db.Column(db.Text)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/matchup_notes', methods=['GET'])
@login_required
def matchup_notes():
    characters = Character.query.all()

    my_id = request.args.get('my', type=int)
    opp_id = request.args.get('opp', type=int)

    matchup_notes = []
    if my_id and opp_id:
        matchup_notes = MatchupNotes.query.filter_by(
            user_id=current_user.id,
            my_character_id=my_id,
            opponent_character_id=opp_id
        ).all()

    all_notes = MatchupNotes.query.filter_by(user_id=current_user.id).all()
    my_char = Character.query.get(my_id) if my_id else None
    opp_char = Character.query.get(opp_id) if opp_id else None

    general_notes = GeneralNotes.query.filter_by(
        user_id=current_user.id,
        opponent_character_id=opp_id
    ).first()

    move_notes = {
        note.move_id: note.content
        for note in MoveMatchupNote.query.filter_by(
            user_id=current_user.id,
            my_character_id=my_id,
            opponent_character_id=opp_id
        ).all()
    }

    return render_template(
        'matchup_notes.html',
        characters=characters,
        my_char=my_char,
        opp_char=opp_char,
        content=None,
        my_id=my_id,
        opp_id=opp_id,
        all_notes=all_notes,
        matchup_notes=matchup_notes,
        move_notes=move_notes,
        general_notes=general_notes
    )

@app.route('/save_move_note', methods=['POST'])
@login_required
def save_move_note():
    move_id = request.form['move_id']
    my_id = request.form['my_character_id']
    opponent_id = request.form['opponent_character_id']
    content = request.form['content']

    note = MoveMatchupNote.query.filter_by(
        user_id=current_user.id,
        move_id=move_id,
        my_character_id=my_id,
        opponent_character_id=opponent_id
    ).first()

    if note:
        note.content = content
    else:
        note = MoveMatchupNote(
            user_id=current_user.id,
            move_id=move_id,
            my_character_id=my_id,
            opponent_character_id=opponent_id,
            content=content
        )
        db.session.add(note)

    db.session.commit()
    flash("Move note saved.")
    return redirect(request.referrer or url_for('matchup_notes'))

@app.route('/save_general_note', methods=['POST'])
@login_required
def save_general_note():
    opponent_id = request.form['opponent_character_id']
    content = request.form['content']

    note = GeneralNotes.query.filter_by(
        user_id=current_user.id,
        opponent_character_id=opponent_id
    ).first()

    if note:
        note.content = content
    else:
        note = GeneralNotes(
            user_id=current_user.id,
            opponent_character_id=opponent_id,
            content=content
        )
        db.session.add(note)

    db.session.commit()
    flash("General note saved.")
    return redirect(request.referrer or url_for('matchup_notes'))

@app.route('/save_matchup_note', methods=['POST'])
@login_required
def save_matchup_note():
    my_id = request.form['my_character_id']
    opponent_id = request.form['opponent_character_id']
    content = request.form['content']

    note = MatchupNotes.query.filter_by(
        user_id=current_user.id,
        my_character_id=my_id,
        opponent_character_id=opponent_id
    ).first()

    if note:
        note.content = content
    else:
        note = MatchupNotes(
            user_id=current_user.id,
            my_character_id=my_id,
            opponent_character_id=opponent_id,
            content=content
        )
        db.session.add(note)

    db.session.commit()
    flash("Matchup note saved.")
    return redirect(request.referrer or url_for('matchup_notes'))


@app.route('/delete_matchup_note', methods=['POST'])
@login_required
def delete_matchup_note():
    my_id = request.form['my_character_id']
    opponent_id = request.form['opponent_character_id']

    note = MatchupNotes.query.filter_by(
        user_id=current_user.id,
        my_character_id=my_id,
        opponent_character_id=opponent_id
    ).first()

    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Matchup note deleted.")
    return redirect(request.referrer or url_for('matchup_notes'))

@app.route('/delete_move_note', methods=['POST'])
def delete_move_note():
    move_id = request.form['move_id']
    my_id = request.form['my_id']
    opp_id = request.form['opp_id']

    MoveMatchupNote.query.filter_by(move_id=move_id, my_character_id=my_id, opponent_character_id=opp_id).delete()
    db.session.commit()
    flash("Move note deleted.")
    return redirect(request.referrer)

@app.route('/delete_general_note', methods=['POST'])
def delete_general_note():
    opponent_id = request.form['opponent_character_id']

    note = GeneralNotes.query.filter_by(
        user_id=current_user.id,
        opponent_character_id=opponent_id
    ).first()

    if note:
        db.session.delete(note)
        db.session.commit()
        flash("General note deleted.")
    return redirect(request.referrer or url_for('matchup_notes'))

@app.route('/delete_all_notes', methods=['POST'])
def delete_all_notes():
    note_type = request.form['note_type']
    my_id = request.form.get('my_character_id')
    opp_id = request.form.get('opp_character_id')

    # Delete all move notes for this matchup
    if note_type == 'move':
        MoveMatchupNote.query.filter_by(user_id=current_user.id, my_character_id=my_id, opponent_character_id=opp_id).delete()

    # Delete the general matchup note
    elif note_type == 'matchup':
        MatchupNotes.query.filter_by(user_id=current_user.id, my_character_id=my_id, opponent_character_id=opp_id).delete()

    db.session.commit()
    flash('All notes for this matchup have been deleted.')
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True)