#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


import dateutil.parser
import babel
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from models import app, db, Venue, Artist, Show
from forms import *
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app.config.from_object('config')
moment = Moment(app)
db.init_app(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

def upcoming_shows(venue_id):
  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
    Show.venue_id == venue_id, Show.artist_id == Artist.id, Show.start_time > datetime.now()).all()
  return upcoming_shows

def upcoming_showsA(artist_id):
  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
    Show.venue_id == Venue.id, Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
  return upcoming_shows

def past_shows(venue_id):
  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
    Show.venue_id == venue_id,Show.artist_id == Artist.id,Show.start_time < datetime.now()).all()
  return past_shows

def past_showsA(artist_id):
  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
    Show.venue_id == Venue.id, Show.artist_id == artist_id, Show.start_time < datetime.now()).all()
  return past_shows
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  locals = []
  venues = Venue.query.all()
  for place in Venue.query.distinct(Venue.city, Venue.state).all():
    locals.append({
      'city': place.city,
      'state': place.state,
      'venues': [{
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': len(upcoming_shows(venue.id))
      } for venue in venues if
          venue.city == place.city and venue.state == place.state]
    })
  return render_template('pages/venues.html', areas=locals)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.

  search = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()
  response = {
    "count": len(venues),
    "data": []
  }
  for venue in venues:
    response["data"].append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': len(upcoming_shows(venue.id))
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  data = {
    'id': venue.id,'name':venue.name, 'genres': venue.genres, 'address': venue.address, 'city': venue.city, 'state': venue.state,
  'phone': venue.phone, 'website': venue.website, 'facebook_link': venue.facebook_link, 'seeking_talent': venue.seeking_talent,
  'image_link': venue.image_link,
    'past_shows': [{
      'artist_id': artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
     } for artist, show in past_shows(venue.id)],
     'upcoming_shows': [{
    'artist_id': artist.id,
    'artist_name': artist.name,
    'artist_image_link': artist.image_link,
    'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
  } for artist, show in upcoming_shows(venue.id)],
  'past_shows_count': len(past_shows(venue.id)),
  'upcoming_shows_count': len(upcoming_shows(venue.id))
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      venue = Venue()
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue was successfully deleted!')
  except:
    db.session.rollback()
    flash('Could not be deleted!')
  finally:
    db.session.close()
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.with_entities(Artist.id,Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.

  search = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()
  response = {
    "count": len(artists),
    "data": []
  }
  for artist in artists:
    response["data"].append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': len(upcoming_showsA(artist.id))
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter_by(id=artist_id).first_or_404()

  data = {
    'id': artist.id, 'name': artist.name, 'genres': artist.genres,  'city': artist.city,'state': artist.state,
          'phone': artist.phone, 'website': artist.website, 'facebook_link': artist.facebook_link,
          'seeking_venue': artist.seeking_venue,'seeking_description':artist.seeking_description, 'image_link': artist.image_link,
    'past_shows': [{
      'venue_id': venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for venue, show in past_showsA(artist.id)],
    'upcoming_shows': [{
      'venue_id': venue.id,
      'venue_name': venue.name,
      'venue_image_link': venue.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for venue, show in upcoming_showsA(artist.id)],
    'past_shows_count': len(past_showsA(artist.id)),
    'upcoming_shows_count': len(upcoming_showsA(artist.id))
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist_data = {
    'id':artist.id,'name':artist.name,'genres':artist.genres,'city':artist.city,'state':artist.state,
    'phone':artist.phone,'website':artist.website,'facebook_link': artist.facebook_link,'seeking_venue':artist.seeking_venue,
    'seeking_description':artist.seeking_description,'image_link': artist.image_link}
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      artist = Artist(artist_id)
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue_data = {
    'id': venue.id, 'name':venue.name, 'genres': venue.genres,'address':venue.address, 'city': venue.city, 'state': venue.state,
    'phone': venue.phone, 'website': venue.website, 'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description, 'image_link': venue.image_link}
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      venue = Venue(venue_id)
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      artist = Artist()
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == Venue.id, Show.artist_id == Artist.id).all()
  shows=Show.query.all()
  data=[]
  for show in shows:
    data.append({'venue_id':show.venue_id,'venue_name':Venue.query.get(show.venue_id).name,'artist_id':show.artist_id,
                 'artist_name': Artist.query.get(show.artist_id).name,'artist_image_link':Artist.query.get(show.artist_id).image_link,
                 'start_time':show.start_time.strftime('%Y-%m-%d %H:%M:%S')})

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  form = ShowForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      show = Show()
      form.populate_obj(show)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except ValueError as e:
      print(e)
      flash('An error occurred. Show could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
