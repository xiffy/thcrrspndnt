import sqlite3
import os
import settings

class Db:
    def __init__(self):
        db_path = settings.CONFIG['db'].get('path', 'data/db.sqlite3')
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path))
