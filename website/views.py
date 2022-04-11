from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Task, City, History
from . import db
from . import config
import json
import datetime
import requests

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        task = request.form.get('task')

        if len(task) < 1:
            flash('Task is too short!', category='error')
        else:
            new_task = Task(data=task, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted!', category='success')

    return jsonify({})

@views.route('/words_search', methods=['GET'])
def words_search():
    return render_template("words_search.html", user=current_user)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&appid={ config.access_token }'
    r = requests.get(url).json()
    return r

@views.route('/weather')
def index_get():
    #cities = City.query.all()
    cities = City.query.filter_by(user_id=current_user.id).all()
    weather_data = []

    for city in cities:

        r = get_weather_data(city.name)
        # print(r)

        tz = datetime.timezone(datetime.timedelta(seconds=int(r['timezone'])))

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'time': datetime.datetime.now(tz = tz).strftime("%m/%d/%Y, %I:%M:%S %p"),
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data, user=current_user)

@views.route('/weather', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
        
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city, user_id=current_user.id)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not exist in the world!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!')

    return redirect(url_for('views.index_get'))

@views.route('weather/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('views.index_get'))


@views.route('/chat', methods=['GET'])
def chat():
    # db.session.query(History).delete()
    # db.session.commit()
    # messages = History.query.all()
    return render_template("chat.html", user=current_user)