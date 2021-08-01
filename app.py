from flask import Flask , render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '8728742384782348273489'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    servers = db.relationship('Server', backref='user', lazy=True)

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80), unique=True, nullable=False)
    about = db.Column(db.String(120), unique=False, nullable=False)
    owner = db.Column(db.String(120), unique=False, nullable=False)

db.create_all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def auth():
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    server = Server.query.all()
    if server: 
        server = server 
    else: 
        server = 'none'
    return render_template('index.html', server = server)

@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first() is not None:
        return 'Username already exists'
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return 'done'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return redirect(url_for('home'))
    else:
        return 'Invalid Credentials'

@app.route('/add_server', methods=['POST'])
@login_required
def add_server():
    name = request.form['name']
    about = request.form['about']
    owner = current_user.username
    user_id = current_user.id
    server = Server(user_id=user_id, name=name, about=about, owner=owner)
    db.session.add(server)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/remove_server/<int:id>')
@login_required
def remove_server(id):
    server = Server.query.filter_by(id=id).first()
    db.session.delete(server)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

# @app.route('/api/users/<int:id>', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)