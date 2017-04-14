from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify
from flask import json
from flask import send_file
from flask import request
import urllib3
import os
from app.models import Movie, db

movies = Blueprint('movies', __name__)
rootUrl = '/juan'

@movies.route('/', methods=['GET'])
def showallmovies():
    movieresults = []
    for i in Movie.query.all():
        movieresults.append(i.serialize())
    response = jsonify(movieresults)
    return response

@movies.route('/search', methods=['GET'])
def findmoviesbyName():
    moviename = request.args.get('name')
    moviecount = Movie.query.filter(Movie.Name.startswith(moviename)).count()
    if moviecount>0:
        movielist = []
        movieresults = Movie.query.filter(Movie.Name.startswith(moviename)).all()
        for i in movieresults:
            movielist.append(i.serialize())
        response = jsonify(movielist)
        return response
    else:
        return render_template('review.html', site=rootUrl), 404

@movies.route('/findmovie', methods=['GET'])
def findmoviebyName():
    moviename = request.args.get('name')
    moviecount = Movie.query.filter_by(Name = moviename).count()
    if moviecount>0:
        movieresult = Movie.query.filter_by(Name = moviename).first()
        response = jsonify(movieresult.serialize());
        return response
    else:
        return render_template('review.html', site=rootUrl), 404

@movies.route('/details.html', methods=['GET'])
def filldetails():
    movieid = request.args.get('id')
    moviecount = Movie.query.filter_by(Id = movieid).count()
    if moviecount>0:
        movie = Movie.query.filter_by(Id = movieid).first()
        return render_template('details.html', name=movie.Name, desc=movie.Description, site=rootUrl)
    else:
        return render_template('reviews.html', site=rootUrl), 404


@movies.route('/get_image', methods=['GET'])
def get_image():
    filename = request.args.get('file')
    file = 'static/poster/' + filename
    return send_file(file, mimetype='image/gif')
    

@movies.route('/add', methods=['POST'])
def handle_fomdata():
        moviename = request.form['name']
        movielength = Movie.query.filter_by(Name = moviename).count()
        if movielength==0 :
            moviedesc = request.form['desc']
            movieposter = request.form['poster']
            try:
		filename = 'app/static/poster/' + moviename + '.jpg'
                http = urllib3.PoolManager()
		r = http.request('GET', movieposter)
		with open(filename, 'wb') as out:
    			out.write(r.data)
		dbmovieposter = '/poster/' + moviename + '.jpg'
            except:
                dbmovieposter = ""            
            nmovie = Movie(moviename, moviedesc, dbmovieposter)
            db.session.add(nmovie)
            db.session.commit()
     
        return "success"
