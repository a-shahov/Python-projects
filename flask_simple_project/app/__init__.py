import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app: Flask = Flask(__name__)
app.config.from_object(Config)  # this is a feature of the flask object

# flask db init - create db
# flask db migrate - generates automatic migrations
# flask db upgrade - to apply the changes to the database
db: SQLAlchemy = SQLAlchemy(app)  # initializing flask extensions
migrate: Migrate = Migrate(app, db)
login = LoginManager(app)

# The 'login' value above is the function (or endpoint) name for the login view. In other words, the name you would
# use in a url_for() call to get the URL.
login.login_view = 'login'

# The SMTP debugging server from python
# python -m smtpd -n -c DebuggingServer localhost:8025
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Server Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # The RotatingFileHandler class is nice because it rotates the logs, ensuring that the log files do not grow too
    # large when the application runs for a long time. In this case I'm limiting the size of the log file to 10KB,
    # and I'm keeping the last ten log files as backup.
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/server.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('test server')

from app import routes, models, errors  # app is directory
