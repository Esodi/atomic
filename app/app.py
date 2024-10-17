#!/usr/bin/python3

# app.py
from flask import Flask, render_template
from models.models import db, User, Competition  # Import User model
from routes.routes import competition_routes
from config import Config
from flask_login import LoginManager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = '/home/egao/Documents'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'txt'}
app.secret_key = 'your_secret_key'  # For flash messages

login_manager = LoginManager()
login_manager.login_view = 'competition_routes.login'
login_manager.init_app(app)

# Initialize the database
db.init_app(app)

# Register Blueprints
app.register_blueprint(competition_routes)

# Create the database tables (run this only once)
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def about():
    return render_template('dash.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/join/<int:competition_id>')
def competition_detail(competition_id):
    competition = Competition.query.get(competition_id)
    if competition is None:
        return "Competition not found", 404
    return render_template('competition_detail.html', competition=competition)

if __name__ == '__main__':
    app.run(debug=True)
