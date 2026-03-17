# All low level functions in here pls
from app import app, db, info, warn
from app.models import User, Post, Message, Transactions, Moderation
import bcrypt  # For password hashing
import smtplib
import ssl

def hash_password(password):
    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    # Check the password against the hashed version
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(email, password, admin):
    try:
        # Firstly, create a class for the user
        user = User(
            email=email,
            password_hash=hash_password(password),
            is_admin=admin
        )
        # Then add to the db and commit
        db.session.add(user)
        db.session.commit()

        # Return status
        info(f"Created new user: {user}")
        return True
    except Exception as e:
        # If something goes wrong, return False
        warn(f"Error creating user: {e}")
        return False

### POSTS ###
def create_post(title, description, skill, post_type, user_id):
    try:
        # Create the post object
        post = Post(
            title=title,
            description=description,
            skill=skill,
            post_type=post_type,
            user_id=user_id
        )
        # Add to db and commit
        db.session.add(post)
        db.session.commit()

        # Return status
        info(f"Created new post: {post}")
        return True
    except Exception as e:
        warn(f"Error creating post: {e}")
        return False
    
def fetch_post(post_id):
    return Post.query.get(post_id)

def update_post(post_id, title=None, description=None, skill=None, post_type=None):
    try:
        # query for post
        post = Post.query.get(post_id)
        if not post:
            warn(f"Post with ID {post_id} not found.")
            return False

        if title is not None:
            post.title = title
        if description is not None:
            post.description = description
        if skill is not None:
            post.skill = skill
        if post_type is not None:
            post.post_type = post_type

        db.session.commit()
        info(f"Post updated: {post}")
        return True
    except Exception as e:
        warn(f"Error updating post: {e}")
        return False
    
def delete_post(post_id):
    try:
        # find post
        post = Post.query.get(post_id)
        if not post:
            warn(f"Post with ID {post_id} not found.")
            return False

        # delete and commit
        db.session.delete(post)
        db.session.commit()
        info(f"Post deleted: {post}")
        return True
    except Exception as e:
        warn(f"Error deleting post: {e}")
        return False

def send_email(to, subject, body):
    # Email config
    port = 465
    password = app.config['EMAIL_PASSWORD']
    smtp_server = app.config['EMAIL_SMTP_SERVER']
    address = app.config['EMAIL_ADDRESS']

    context = ssl.create_default_context()

    try:
        # try sending
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(address, password)
            server.sendmail(address, to, f"From: {address}\nTo: {to}\nSubject: {subject}\n\n{body}\n")

        return True
    except Exception as e:
        warn(f"Error sending email: {e}")
        return False