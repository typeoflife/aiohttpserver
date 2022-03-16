from datetime import datetime

from gino import Gino

db = Gino()
PG_DATABASE = 'postgresql+asyncpg://postgres:***@127.0.0.1:5432/aiohttp'

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    __idx_1 = db.Index('app_username', 'username')


class AdvModel(db.Model):
    __tablename__ = 'adv'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
