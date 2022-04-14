"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def view_homepage():
    """The homepage"""

    return render_template('homepage.html')


@app.route('/movies')
def view_movies():
    """Show all movies"""

    movies = crud.show_all_movies()

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def view_movie(movie_id):
    """show movie details"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/movies/<int:movie_id>', methods = ["POST"])
def submit_rating(movie_id):
    #check if user is logged in (session)
        #flash if not logged in
    #add the rating to the db crud.create_rating
        #flash success

    #TODO query for movie to pass in - not movie_id
    
    session_user = session.get('user_id', False)
    
    if session_user:
        score = int(request.form.get('score'))
        movie = crud.get_movie_by_id(movie_id)
        user = crud.get_user_by_id(session_user)
        rating = crud.create_rating(user, movie, score)
        db.session.add(rating)
        db.session.commit()
        flash(f"You have rated this movie with a {score}.")
        #flash(f"Score = {score}, movie_id = {movie_id}, user = {user_id}")
    else:
        flash('You must be logged in to rate movies.')


    return redirect(f'/movies/{movie_id}')

@app.route('/users')
def view_users():
    """Show all users"""

    users = crud.get_all_users()

    return render_template('all_users.html', users=users)


@app.route('/users', methods=['POST'])
def register_user():
    """Register a user"""

    email = request.form.get('email')
    password = request.form.get('password')

    if (crud.get_user_by_email(email)):
        flash('User already exists')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')

    return redirect('/')


@app.route('/login', methods=["POST"])
def user_login():
    """Verify user login"""

    email = request.form.get('email')
    password = request.form.get('password')

    verified_user = crud.verify_user(email, password)

    if verified_user:
        session['user_id'] = verified_user.user_id
        flash("Logged in!")
    else:
        flash('Login unsuccesful!')

    return redirect('/')

@app.route('/users/<user_id>')
def view_user(user_id):
    """Show a user"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
