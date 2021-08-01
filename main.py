from flask import Flask , render_template, request, redirect, url_for
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(120))

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    about = db.Column(db.String(120))
    owner = db.Column(db.Integer)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    about = db.Column(db.String(120))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer)
    message = db.Column(db.String(120))
    messenger = db.Column(db.String(120))

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
    server = Server.query.filter_by(owner=current_user.id).all()
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
    owner = current_user.id
    server = Server(name=name, about=about, owner=owner)
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

@app.route('/server/<int:id>')
@login_required
def server(id):
    server = Server.query.filter_by(id=id).first()
    if server:
        channel = Channel.query.filter_by(server_id=id).all()
        if channel: 
            return render_template('server.html', server=server, channel=channel)
        else:
            channel = None
            return render_template('server.html', server=server, channel=channel)
    else:
        return 'Server not found'

@app.route('/add_channel/<int:id>', methods=['POST'])
@login_required
def add_channel(id):
    channel = request.form['channel']
    about = request.form['about']
    new = Channel(name = channel, about = about, server_id = id)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('server', id=id))

@app.route('/server/<int:server_id>/channel/<int:channel_id>')
@login_required
def channel(server_id, channel_id):
    server = Server.query.filter_by(id=server_id).first()
    channel = Channel.query.filter_by(id=channel_id).first()
    if server and channel:
        messages = Message.query.filter_by(channel_id=channel_id).all()
        if messages:
            return render_template('channel.html', server=server, channel=channel, messages=messages)
        else:
            messages = None
            return render_template('channel.html', server=server, channel=channel, messages=messages)
    else:
        return 'Channel not found'

@app.route('/server/<int:server_id>/channel/<int:channel_id>/message', methods=['POST'])
@login_required
def add_message(server_id, channel_id):
    message = request.form['message']
    messenger = current_user.username
    new = Message(channel_id = channel_id , message=message, messenger=messenger)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('channel', server_id=server_id, channel_id=channel_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

# @app.route('/api/users/<int:id>', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)