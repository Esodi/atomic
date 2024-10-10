#!/usr/bin/python3
'''flask app '''


from flask import Blueprint, render_template, request, flash, redirect, url_for,Flask
#from app.forms.competition_forms import CompetitionForm
#from app.services.competition_service import CompetitionService
#from app.utils.decorators import login_required

#competitions_bp = Blueprint('competitions', __name__)

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/competitions')
def list_competitions():
    competitions = CompetitionService.get_all_competitions()
    return render_template('competitions/list.html', competitions=competitions)

@app.route('/competitions/create', methods=['GET', 'POST'])
@login_required
def create_competition():
    form = CompetitionForm()
    if form.validate_on_submit():
        CompetitionService.create_competition(form.data)
        flash('Competition created successfully!', 'success')
        return redirect(url_for('competitions.list_competitions'))
    return render_template('competitions/create.html', form=form)

if __name__ == '__main__':
    app.run()
