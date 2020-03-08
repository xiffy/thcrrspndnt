import sqlite3
import os

class Db:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 'data/db.sqlite3'))
