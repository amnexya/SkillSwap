from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import sys
import argparse

# Colouring for terminal logs
@dataclass
class Colours:
    """Hold the ASCII escape sequences for printing colours."""

    red: str = "\033[31m" # Fatal Errors
    endc: str = "\033[m"
    green: str = "\033[32m" # Info
    yellow: str = "\033[33m" # Non-fatal warnings
    blue: str = "\033[34m" # Log info

def die(message: str) -> None:
    """This is a function to exit the program with an error message."""

    print(f"{Colours.red}[ERROR]{Colours.endc} {message}", file=sys.stderr)
    exit(1)


def info(message: str) -> None:
    """This function allows for formatted information in a log.

    Args:
        message (str): Information to be printed
    """

    print(f"{Colours.blue}[INFO]{Colours.endc} {message}")


def warn(message: str) -> None:
    """This function allows for formatted warnings in a log.

    Args:
        message (str): Warnings to be printed
    """
    print(f"{Colours.yellow}[WARN]{Colours.endc} {message}")

# Parse arguments given in command line
def parse_args() -> argparse.Namespace:
    """This function parses the arguments given in the command line.

    Returns:
        argparse.Namespace: The arguments given in the command line.
    """

    parser = argparse.ArgumentParser(description="Run the SkillSwap Flask application.")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run the application in debug mode (development mode).",
    )
    parser.add_argument(
        "--env",
        type=str,
        action="store",
        help="Specify the location of .env"
    )
    return parser.parse_args()

info("Parsing command line arguments...")
args = parse_args()

# This just sets the directory we're running in, so we can find the .env file and other files we need
basedir = os.path.abspath(os.path.dirname(__file__))

info("Checking .env")
# Has env been specified in launch args?
if args.env:
    info(f"Using .env file at {args.env}")
    env = args.env
else:
    # If not, use default and warn
    info("No .env location specified, using default.")
    env = os.path.join(basedir, ".env")

# Check if the file exists
if os.path.exists(env):
    info(f"Found .env file at {env}")
else:
    # If not then kill
    die(f"Could not find .env file at {env}, please add one and relaunch. Refer to docs for info.")

# Load the environment variables from the .env file
load_dotenv(env)

# Lets get to starting flask and db
info("Starting Flask app...")
app = Flask(__name__)

info("Adding Flask config")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() in ("true", "1", "t")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['EMAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
app.config['EMAIL_SMTP_SERVER'] = os.environ.get("EMAIL_SMTP_SERVER")
app.config['EMAIL_ADDRESS'] = os.environ.get("EMAIL_ADDRESS")

info("Starting DB")
db = SQLAlchemy(app)

info("Starting DB migration tool")
migrate = Migrate(app, db)

#info("Starting Login Manager")
#login = LoginManager(app)

# Import the routes and models so they are registered with the app
from app import routes, models