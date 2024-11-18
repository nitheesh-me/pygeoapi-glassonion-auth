from pathlib import Path
from flask import g
from flask_login import LoginManager, login_required
from flask_authorize import Authorize, PermissionsMixin
from flask_sqlalchemy import SQLAlchemy
import uuid

from .util import enable_mock
enable_mock()
from .views import account
from pygeoapi.flask_app import APP, CONFIG


GITHUB = True


APP.register_blueprint(account, url_prefix='/account')
from .managers.login import init_github_login
init_github_login(APP)


#### DB setup START
from .managers.db import db
APP.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db.init_app(APP)
with APP.app_context():
    db.create_all()
#### DB setup END


from .managers.login import login_manager, User
APP.config['SECRET_KEY'] = uuid.uuid4().hex
login_manager.init_app(APP)


# class User(db.Model, PermissionsMixin):
#     id = db.Column('student_id', db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     roles = db.relationship('Role', secondary='user_roles')

# class Role(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)

# class UserRoles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))


from .injectors.templates import add_template_location
add_template_location(CONFIG, (Path(__file__).parent / 'templates').resolve())

from .injectors.route import apply_decorator_on_views
apply_decorator_on_views(
        APP, login_required,
        include={
            'pygeoapi.*', 'account.settings', 'account.logout',
            '!pygeoapi.landing_page', '!pygeoapi.openapi', 'pygeoapi.static',
        }
    )
from .managers.login import required_github_login
apply_decorator_on_views(
    APP, required_github_login,
    include={'admin.*'}
)


authorize = Authorize(APP)

from pprint import pprint
pprint(APP.view_functions)

pprint(APP.jinja_loader.list_templates())
