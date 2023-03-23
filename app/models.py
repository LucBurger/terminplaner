from datetime import datetime, time
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

mitglieder = db.Table('mitglieder',
    db.Column('mitglieder_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('mitglied_id', db.Integer, db.ForeignKey('team.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    mitglied = db.relationship(
        'Team', secondary=mitglieder,
        primaryjoin=(mitglieder.c.mitglieder_id == id),
        secondaryjoin=(mitglieder.c.mitglied_id == id),
        backref=db.backref('mitglieder', lazy='dynamic'), lazy='dynamic', viewonly=True
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0   
    
    def beitreten(self, team):
        if not self.is_member(team):
            self.mitglied.append(team)

    def austreten(self, team):
        if self.is_member(team):
            self.mitglied.remove(team)

    def is_member(self, team):
        return self.mitglied.filter(
            mitglieder.c.mitglied_id == team.id).count() > 0 

    def member_of_teams(self):
        mitglied = Team.query.join(
            mitglieder, (mitglieder.c.mitglied_id == Team.id)).filter(
                mitglieder.c.mitglieder_id == self.id)

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
     
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(64), index=True, unique=True)
    termine = db.relationship('Termin', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team {}>'.format(self.teamname)

    def avatar(self, size):
        digest = md5(self.teamname.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
class Termin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    terminname = db.Column(db.String(64))
    datum = db.Column(db.DateTime)
    zeit = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Termin {} vom {} um {} für team_id {}>'.format(self.terminname, self.datum, self.zeit, self.team_id)