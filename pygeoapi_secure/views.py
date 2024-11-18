from flask import Blueprint, get_flashed_messages, redirect, url_for, request, render_template, flash
from flask_login import login_user, logout_user, current_user
from pygeoapi.flask_app import execute_from_flask
from pygeoapi.api import F_HTML, F_JSONLD
from flask_authorize import PermissionsMixin

from .util import render_j2_template


account = Blueprint('account', __name__, template_folder='templates')


# Protect routes starting with '/settings' using the before_request hook
@account.before_request
def check_account_authentication():
    # Only check accountentication for routes that start with '/settings'
    if request.endpoint and request.endpoint.startswith('settings') and not current_user.is_accountenticated:
        return redirect(url_for('login'))  # Redirect to login if not accountenticated


class SettingsView(PermissionsMixin):
    def __init__(self):
        self.permissions = {'read': 'settings:read'}

    def settings(self):
        self.authorize('read')
        return "This is the settings page."

settings_view = SettingsView()
account.add_url_rule('/settings', view_func=settings_view.settings)


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except Exception:
        return redirect(fallback)
    return redirect(dest_url)

# Route to handle user login
@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        from .managers.login import users, User
        # Validate the user credentials (you would replace this with a real DB check)
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect_dest(url_for('account.settings'))
        flash('Invalid username or password')
    return execute_from_flask(
        login_f,
        request,
    )

def login_f(
        api,
        request,
):
    if request.format == F_HTML:  # render
        flashed_messages = get_flashed_messages()
        print(flashed_messages)
        content = render_j2_template(
            api.tpl_config,
            'account/login.html',
            {
                'flashed_messages': flashed_messages,
            },
            request.locale
        )
        headers = {'Content-Type': 'text/html'}
        return headers, 200, content

    return {}, 200, {'message': 'Login page must be here, maybe in HTML?'}


@account.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pygeoapi.landing_page'))
