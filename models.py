from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy()
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venue'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String,nullable=False)
  city = db.Column(db.String(120),nullable=False)
  state = db.Column(db.String(120),nullable=False)
  address = db.Column(db.String(120),nullable=False)
  phone = db.Column(db.String(120),nullable=False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website=db.Column(db.String(120))
  seeking_talent=db.Column(db.Boolean)
  genres = db.Column(db.ARRAY(db.String(120)))
  seeking_description=db.Column(db.String(250))
  shows = db.relationship('Show', backref="venue", lazy=True)




    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artist'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String,nullable=False)
  city = db.Column(db.String(120),nullable=False)
  state = db.Column(db.String(120),nullable=False)
  phone = db.Column(db.String(120),nullable=False)
  genres =  db.Column(db.ARRAY(db.String(120)))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean)
  seeking_description=db.Column(db.String(250))
  shows = db.relationship('Show', backref="artist", lazy=True)


class Show(db.Model):
  _tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# db.create_all()
# I'm sorry. I do run the app before doing 'flask db migrate' .  warnings.warn(FSADeprecationWarning(
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.ddl.postgresql] Detected sequence named 'show_id_seq' as owned by integer column 'show(id)', assuming SERIAL and omitting
# INFO  [alembic.env] No changes in schema detected.
# So I tried to wipe what I added and run. After that repeat again the add. Sorry, as what you did is considered stupid.
