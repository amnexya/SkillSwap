# This file allows our db to be set up and used.
# We should be able to update and migrate in init, will have to check though.

from flask_login import UserMixin
from app import db
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # user id
    email = db.Column(db.String(255), index=True, unique=True) # email
    password_hash = db.Column(db.String(255)) # hashed and salted passwd
    balance = db.Column(db.Float, default=10.0) # Starting balance for new users
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc)) # Account creation time
    is_admin = db.Column(db.Boolean, default=False) # Admin status

    def __repr__(self):
        return f'<User {self.email}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # post id
    title = db.Column(db.String(140)) 
    description = db.Column(db.Text)
    skill = db.Column(db.String(255)) # skill person is giving or wanting
    post_type = db.Column(db.String(50))  # 'offer' or 'request'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Post {self.title}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.recipient_id}>'

class Transactions(db.Model): # transactions are subject to simulated escrow, funds are held until recipient confirms receipt
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Transaction from {self.sender_id} to {self.recipient_id} of {self.amount}>'
    
class Moderation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id')) # Post in question
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Target user
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who took the action
    action = db.Column(db.String(50))  # 'flagged', 'removed', etc.
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Moderation action {self.action} on post {self.post_id} by user {self.user_id}>'