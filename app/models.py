from . import db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = ['Superuser', 'Admin']
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(64), unique=True, index=True)
    email = db.Column(db.UnicodeText(), nullable=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password cannot be read directly')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def add_initial_login():
        username = current_app.config['SUPERUSER_NAME']
        password = current_app.config['SUPERUSER_PASSWORD']
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is None:
                user = User(username=username)
                user.password = password
                user.role = Role.query.filter_by(name='Superuser').first()
                db.session.add(user)
                db.session.commit()


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(40), nullable=False, default=uuid.uuid4())
    phrase = db.Column(db.UnicodeText)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    is_locked = db.Column(db.Boolean, default=True, nullable=False)
    contestants = db.relationship('Contestant', backref='game')

    def __repr__(self):
        return '<Game %r>' % self.phrase


class Contestant(db.Model):
    __tablename__ = 'contestant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText)
    uuid = db.Column(db.String(40), nullable=False, default=uuid.uuid4())
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Contestant %r>' % self.name
