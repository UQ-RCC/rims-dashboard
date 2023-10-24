from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import rimsboard.config as config

"""
#we're using flask, so need to use from flask import SQLAlchemy
#somewhat recursive, need to pass the top-level app instance down to db

#pitschi code uses sqlalchemy directly - need to manage the sessions
by passing (db: Session = Depends(pdb.get_db))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database'
db = SQLAlchemy(app)

"""


SQLALCHEMY_DATABASE_URL = (f"{config.get('database', 'type')}://"
                           f"{config.get('database', 'username')}:"
                           f"{config.get('database', 'password')}@"
                           f"{config.get('database', 'host')}/"
                           f"{config.get('database', 'name')}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

Base = declarative_base()