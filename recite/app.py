import os
import datetime
from flask import Flask
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *


APP_DIR = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)
app.config.from_object(__name__)

DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'recite.db')
DEBUG = False

flask_db = FlaskDB(app)

database = flask_db.database

class Entry(flask_db.Model):
    content = TextField()
    translation = TextField()
    memo = TextField()
    created = DateTimeField(default=datetime.datetime.now, index=True)

def main():
    database.create_tables([], safe=True)
    app.run(debug=True)

if __name__ == '__main__':
    main()


