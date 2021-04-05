from . import db
import uuid


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<User %r>' % self.username


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
