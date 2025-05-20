import datetime
from flask_sqlalchemy import SQLAlchemy

today = datetime.date.today().strftime("%d-%m-%Y")
db = SQLAlchemy()