from datetime import datetime, time
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

#Eigenentwicklung
mitglieder = db.Table('mitglieder',
    db.Column('mitglieder_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('mitglied_id', db.Integer, db.ForeignKey('team.id'))
)

#Übernommen aus den Beispielen mit Anpassungen
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    mitglied = db.relationship('Team', secondary=mitglieder, backref=db.backref('mitglied_von'))

#Übernommen aus den Beispielen
    def __repr__(self):
        return '<User {}>'.format(self.username)

#Übernommen aus den Beispielen
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

#Übernommen aus den Beispielen
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Übernommen aus den Beispielen    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

#Eigenentwicklung
    def beitreten(self, team):
        self.mitglied.append(team)

#Eigenentwicklung
    def austreten(self, team):
        self.mitglied.remove(team)

#Eigenentwicklung
    def member_of_teams(self):
        mitglied = Team.query.join(
            mitglieder, (mitglieder.c.mitglied_id == Team.id)).filter(
                mitglieder.c.mitglieder_id == self.id)

#Eigenentwicklung    
    def mitglied_teams(self):
        mitglied = Team.query.join(
            mitglieder, (mitglieder.c.mitglied_id == Team.mitglieder)).filter(
                mitglieder.c.mitglieder_id == self.id)
        return mitglied.order_by(Team.id.asc())

 #Übernommen aus den Beispielen   
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

#Übernommen aus den Beispielen    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

#Übernommen aus den Beispielen     
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#Eigenentwicklung
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(64), index=True, unique=True)
    beschreibung = db.Column(db.String(140))
    termine = db.relationship('Termin', backref='team_termine', lazy='dynamic')

    def __repr__(self):
        return '<Team {} {}>'.format(self.teamname, self.beschreibung)

    def avatar(self, size):
        digest = md5(self.teamname.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

#Eigenentwicklung 
class Termin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    terminname = db.Column(db.String(64))
    beschreibung = db.Column(db.String(140))
    datum = db.Column(db.Date)
    zeit = db.Column(db.Time)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Termin {} vom {} um {} für team_id {}>'.format(self.terminname, self.datum, self.zeit, self.team_id)