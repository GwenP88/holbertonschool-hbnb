from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/places/<place_id>')
def place(place_id):
    return render_template('place.html')

@main.route('/user')
def user():
    return render_template('user.html')
