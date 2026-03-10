# All low level functions in here pls
from app import app, db, info, warn
from app.models import User, Post, Message, Transactions, Moderation
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(email, password, admin):
    try:
        # Firstly, create a class for the user
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
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