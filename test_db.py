from datetime import datetime

from models import UploadModel
from database_manager import DatabaseManager
from database_manager.conditions import Conditions

if __name__ == '__main__':
    db = DatabaseManager()
    db.connect('diskord.db')

    try:
        u = UploadModel(user_id='1', size=1024, upload_time=datetime.now())
        print(db.select('uploads', UploadModel, row_limit=10, conditions=Conditions(user_id=1)))
        # db.insert('uploads', u)
        # print(db.select('uploads', Upload, row_limit=10))
    finally:
        db.close()
