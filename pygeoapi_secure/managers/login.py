import logging
import os
from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import LoginManager, UserMixin, AnonymousUserMixin
from .db import User
from pygeoapi.api import F_HTML

LOGGER = logging.getLogger(__name__)

login_manager = LoginManager()

users = {'user1': {'password': 'password1'}}


# Define a User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    ## How to load the user details?
    try:
        return User(user_id)
    except Exception as e:
        LOGGER.error(f'Error loading user: {e}')
        return None


@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('account.login', next=request.endpoint))


from flask_dance.contrib.github import make_github_blueprint, github


def init_github_login(app):
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
    app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
    github_bp = make_github_blueprint()
    app.register_blueprint(github_bp, url_prefix="/account-ex")


def required_github_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not github.authorized:
            return redirect(url_for("github.login"))
        return func(*args, **kwargs)
    return wrapper
