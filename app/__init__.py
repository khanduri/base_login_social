from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from celery import Celery
from sendgrid import SendGridClient
from flask_admin import Admin
from hashids import Hashids


app = Flask(__name__, static_folder='../static')
app.config.from_object('config')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf['CELERY_IMPORTS'] = (
    'app.tasks',
)

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

sg = SendGridClient(app.config['SENDGRID_USER'], app.config['SENDGRID_API_KEY'])

hashids = Hashids(salt=app.config.get('HASHIDS_SALT'), min_length=8)


from app import views, tables


class UserView(views.AdminAccessView):
        can_delete = False


class PostView(views.AdminAccessView):
        page_size = 50


admin = Admin(app, name='Admin Home', template_mode='bootstrap3', index_view=views.AdminAccessIndexView())
admin.add_view(UserView(tables.User, db.session))
admin.add_view(PostView(tables.Post, db.session))