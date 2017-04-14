from flask import Blueprint
from flask import request
from flask import render_template
from app.models import Movie, db, Review

main = Blueprint('main', __name__)
rootUrl = '/juan'

@main.route('/', methods=['GET'])
def hello_world():
    return render_template('reviews.html', site=rootUrl)
