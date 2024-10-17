#!/usr/bin/python3

# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from models.models import db, Competition, User, UserCompetition
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from io import BytesIO
from datetime import datetime

# Create a Blueprint for competition-related routes
competition_routes = Blueprint('competition_routes', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@competition_routes.route('/create_competition', methods=['GET', 'POST'])
@login_required
def create_competition():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        details = request.form['details']
        fee = request.form['fee']
        date = request.form['date']
        location = request.form['location']
        prizes = request.form['prizes']

        try:
            fee = float(fee)  # Ensure fee is a valid number
            new_competition = Competition(
                name=name,
                description=description,
                fee=fee,
                details=details,
                date=date,         # New attribute
                location=location, # New attribute
                prizes=prizes,     # New attribute
                creator_id=current_user.id
            )
            db.session.add(new_competition)
            db.session.commit()
            flash('Competition created successfully!', 'success')
            return redirect(url_for('competition_routes.user_dashboard'))
        except ValueError:
            flash('Please enter a valid fee.', 'danger')
    
    return render_template('create_competition.html')

# @competition_routes.route('/competitions', methods=['GET'])
# @login_required
# def get_competitions():
#     # Get competitions specific to the logged-in user
#     user = current_user
#     user_competitions = Competition.query.join(UserCompetition).filter(UserCompetition.user_id == user.id).all()
#     return render_template('dash.html', user=user, competitions=user_competitions)

@competition_routes.route('/all_competitions', methods=['GET'])
@login_required
def get_all_competitions():
    competitions = Competition.query.all()
    return render_template('competitions_list.html', competitions=competitions)

@competition_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('competition_routes.signup'))

        # Use pbkdf2:sha256 for password hashing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully! Please log in.', 'success')
        return redirect(url_for('competition_routes.login'))
    
    return render_template('signup.html')

@competition_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            # Redirect the user to their personal dashboard
            return redirect(url_for('competition_routes.user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@competition_routes.route('/dashboard', methods=['GET'])
@login_required
def user_dashboard():
    # Get the logged-in user's information and competitions
    user = current_user
    user_competitions = Competition.query.join(UserCompetition).filter(UserCompetition.user_id == user.id).all()
    all_competitions = Competition.query.all()
    return render_template('dash.html', user=user, user_competitions=user_competitions, competitions=all_competitions)

@competition_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('competition_routes.login'))

def save_user_competition(user, competition, status='joined'):
    """
    Save the user's competition join information.
    """
    user_competition = UserCompetition(
        user_id=user.id,
        competition_id=competition.id,
        status=status
    )
    db.session.add(user_competition)
    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

@competition_routes.route('/join_competition/<int:competition_id>', methods=['GET', 'POST'])
@login_required
def join_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    user = current_user

    # Check if the user is already participating in this competition
    existing_participation = UserCompetition.query.filter_by(user_id=user.id, competition_id=competition.id).first()
    if existing_participation:
        flash('You are already participating in this competition.', 'info')
        return redirect(url_for('competition_routes.user_dashboard'))

    if request.method == 'POST':
        if save_user_competition(user, competition):
            flash(f'You have successfully joined the competition: {competition.name}', 'success')
        else:
            flash('An error occurred while joining the competition. Please try again.', 'danger')
        return redirect(url_for('competition_routes.user_dashboard'))
    
    # If it's a GET request, show the confirmation page
    return render_template('join_confirmation.html', competition=competition)

@competition_routes.route('/leave_competition/<int:competition_id>', methods=['POST'])
@login_required
def leave_competition(competition_id):
    user = current_user
    user_competition = UserCompetition.query.filter_by(user_id=user.id, competition_id=competition_id).first()
    
    if user_competition:
        db.session.delete(user_competition)
        try:
            db.session.commit()
            flash('You have successfully left the competition.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while leaving the competition. Please try again.', 'danger')
    else:
        flash('You are not participating in this competition.', 'info')
    
    return redirect(url_for('competition_routes.user_dashboard'))

# routes/routes.py

@competition_routes.route('/submit_project/<int:competition_id>', methods=['GET', 'POST'])
@login_required
def submit_project(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    user = current_user

    # Check if the user is participating in this competition
    user_competition = UserCompetition.query.filter_by(user_id=user.id, competition_id=competition.id).first()
    if not user_competition:
        flash('You are not participating in this competition.', 'danger')
        return redirect(url_for('competition_routes.user_dashboard'))

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'projectFile' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['projectFile']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            project_description = request.form.get('projectDescription')
            if not project_description:
                flash('Please provide a project description.', 'danger')
                return redirect(request.url)

            # Save file data to database
            file_data = file.read()
            file_mimetype = file.mimetype

            # Debug statements to verify file data
            print(f"Filename: {filename}")
            print(f"File mimetype: {file_mimetype}")
            print(f"File data length: {len(file_data)}")

            # Update the user's competition entry with the project details
            user_competition.project_description = project_description
            user_competition.project_file_name = filename
            user_competition.project_file_data = file_data
            user_competition.project_file_mimetype = file_mimetype
            user_competition.submission_date = datetime.utcnow()

            try:
                db.session.commit()
                flash('Project submitted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while submitting the project. Please try again.', 'danger')
            
            return redirect(url_for('competition_routes.user_dashboard'))
        else:
            flash('File type not allowed', 'danger')
            return redirect(request.url)
        
    return render_template('submit_project.html', competition=competition)

@competition_routes.route('/view_submissions/<int:competition_id>')
@login_required
def view_submissions(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    
    # Check if the current user is the creator of the competition
    if competition.creator_id != current_user.id:
        flash('You do not have permission to view these submissions.', 'danger')
        return redirect(url_for('competition_routes.user_dashboard'))
    
    submissions = UserCompetition.query.filter_by(competition_id=competition_id).all()
    return render_template('view_submissions.html', competition=competition, submissions=submissions)

@competition_routes.route('/download_submission/<int:submission_id>')
@login_required
def download_submission(submission_id):
    submission = UserCompetition.query.get_or_404(submission_id)
    
    # Check if the current user is the creator of the competition
    if submission.competition.creator_id != current_user.id:
        abort(403)  # Forbidden
    
    # Check if project_file_data is available
    if submission.project_file_data is None:
        flash('No file data available for download.', 'danger')
        return redirect(url_for('competition_routes.view_submissions', competition_id=submission.competition_id))

    return send_file(
        BytesIO(submission.project_file_data),
        mimetype=submission.project_file_mimetype,
        as_attachment=True,
        download_name=submission.project_file_name or 'download'  # Default name if None
    )


@competition_routes.route('/submit_winners/<int:competition_id>', methods=['GET', 'POST'])
@login_required
def submit_winners(competition_id):
    competition = Competition.query.get_or_404(competition_id)

    # Ensure that only the competition creator can access this page
    if competition.creator_id != current_user.id:
        flash('You do not have permission to submit winners for this competition.', 'danger')
        return redirect(url_for('competition_routes.user_dashboard'))

    participants = UserCompetition.query.filter_by(competition_id=competition_id).all()

    if request.method == 'POST':
        # Get the list of selected winners' IDs from the form
        selected_winner_ids = request.form.getlist('winner_ids')

        if not selected_winner_ids:
            flash('Please select at least one winner.', 'danger')
            return redirect(request.url)

        # Update the status of the selected winners
        for user_competition in participants:
            if str(user_competition.user_id) in selected_winner_ids:
                user_competition.status = 'winner'  # Mark as a winner
            else:
                user_competition.status = 'participant'  # Ensure others remain as participants

        try:
            db.session.commit()
            flash('Winners submitted successfully!', 'success')
            return redirect(url_for('competition_routes.view_submissions', competition_id=competition_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the winners. Please try again.', 'danger')
            return redirect(request.url)

    return render_template('submit_winners.html', competition=competition, participants=participants)

@competition_routes.route('/view_winners/<int:competition_id>', methods=['GET'])
@login_required
def view_winners(competition_id):
    # Get the competition details
    competition = Competition.query.get_or_404(competition_id)

    # Ensure that only the competition creator or participants can access this page
    if competition.creator_id != current_user.id:
        flash('You do not have permission to view the winners of this competition.', 'danger')
        return redirect(url_for('competition_routes.user_dashboard'))

    # Get the winners of the competition
    winners = UserCompetition.query.filter_by(competition_id=competition_id, status='winner').all()

    return render_template('view_winners.html', competition=competition, winners=winners)
