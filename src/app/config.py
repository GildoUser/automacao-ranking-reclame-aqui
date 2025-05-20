from src.app.database import today
class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{today}.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False