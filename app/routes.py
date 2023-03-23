from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, EditProfileForm, CreateTeam, CreateTermin
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Team, Termin
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, EmptyForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email

#Übernommen aus den Beispielen
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    teams = Team.query.order_by(Team.id.desc()).paginate(
        page=page, per_page=app.config['TEAMS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=teams.next_num) \
        if teams.has_next else None
    prev_url = url_for('index', page=teams.prev_num) \
        if teams.has_prev else None
    termine = Termin.query.order_by(Termin.id.desc())
    return render_template('index.html', title='Home',
                           next_url=next_url,
                           prev_url=prev_url, teams=teams, termine=termine)

#Übernommen aus den Beispielen
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#Übernommen aus den Beispielen
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Übernommen aus den Beispielen
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#Übernommen aus den Beispielen
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title=user.username, user=user)

#Übernommen aus den Beispielen
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

#Übernommen aus den Beispielen
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

#Übernommen aus den Beispielen
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

#Eigenentwicklung
@app.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():
    form = CreateTeam()
    if form.validate_on_submit():
        team = Team(teamname=form.teamname.data, beschreibung=form.beschreibung.data)
        db.session.add(team)
        db.session.commit()
        flash('Congratulations, your team is now registered!')
        return redirect(url_for('teams'))
    page = request.args.get('page', 1, type=int)
    teams = Team.query.order_by(Team.id.asc()).paginate(
        page=page, per_page=app.config['TEAMS_PER_PAGE'], error_out=False)
    next_url = url_for('teams', page=teams.next_num) \
        if teams.has_next else None
    prev_url = url_for('teams', page=teams.prev_num) \
        if teams.has_prev else None
    return render_template("teams.html", title='Teams', form=form, teams=teams, next_url=next_url, prev_url=prev_url)

#Eigenentwicklung
@app.route('/teams/<teamname>')
@login_required
def team(teamname):
    team = Team.query.filter_by(teamname=teamname).first_or_404()
    form = EmptyForm()
    return render_template('team.html', title=team.teamname, team=team, form=form, user=user)

#Eigenentwicklung
@app.route('/teams/<teamname>/beitreten/', methods=['POST'])
@login_required
def beitreten(teamname):
    form = EmptyForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(teamname=teamname).first()
        if team is None:
            flash('Team {} not found.'.format(teamname))
            return redirect(url_for('index'))
        current_user.beitreten(team)
        db.session.commit()
        flash('Du bist {} beigetreten!'.format(teamname))
        return redirect(url_for('team', teamname=teamname))
    else:
        return redirect(url_for('index'))

#Eigenentwicklung   
@app.route('/teams/<teamname>/austreten', methods=['POST'])
@login_required
def austreten(teamname):
    form = EmptyForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(teamname=teamname).first()
        if team is None:
            flash('User {} not found.'.format(teamname))
            return redirect(url_for('index'))
        current_user.austreten(team)
        db.session.commit()
        flash('Du bist nicht mehr im Team {}.'.format(teamname))
        return redirect(url_for('team', teamname=teamname))
    else:
        return redirect(url_for('index'))

#Eigenentwicklung    
@app.route('/teams/<teamname>/termine', methods=['GET'])
@login_required
def termin(teamname):
    team = Team.query.filter_by(teamname=teamname).first_or_404()
    termine = Termin.query.filter_by(team_id=team.id).order_by(Termin.datum.asc())
    return render_template('termin.html', titel='Termine', termine=termine, team=team)

#Eigenentwicklung
@app.route('/teams/<teamname>/termine/erstellen', methods=['GET', 'POST'])
@login_required
def termin_erstellen(teamname):
    team = Team.query.filter_by(teamname=teamname).first_or_404()
    form = CreateTermin()
    if form.validate_on_submit():
        termin = Termin(terminname=form.terminname.data, beschreibung=form.beschreibung.data, datum=form.datum.data, zeit=form.zeit.data, team_id=team.id)
        db.session.add(termin)
        db.session.commit()
        flash('Congratulations, your termin is online!')
        return redirect(url_for('termin', teamname=teamname))
    termine = Termin.query.filter_by(team_id=team.id).first()
    return render_template('termin_erstellen.html', titel="Termin erstellen", termine=termine, form=form, team=team)