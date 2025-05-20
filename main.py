import os
from src.app import create_app
from src.app.database import today
from src.web_hunter.WebHunter import WebHunter
from src.waiter.waiter import Waiter

from src.app.database import db

file_exists = os.path.isfile(f"./instance/{today}.db")

app = create_app()
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        web_hunter = WebHunter(db,file_exists)
        topic_data = web_hunter.verifyFile()
        Waiter(topic_data,web_hunter).startService()

        
