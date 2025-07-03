from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'patdabaker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

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

if __name__ == '__main__':
    app.run(debug=True)