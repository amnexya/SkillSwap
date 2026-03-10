from app import app, db
from app.models import User, Post, Message, Transactions, Moderation
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
#from app.forms import LoginForm, RegistrationForm, PostForm, MessageForm
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")