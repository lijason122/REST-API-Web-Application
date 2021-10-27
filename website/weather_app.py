import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy 
from .models import User, City
from . import db
import datetime

weather_app = Blueprint('weather_app', __name__)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&appid=611704fdbfc4115106a7f01d8ffd396a'
    r = requests.get(url).json()
    return r

@weather_app.route('/weather')
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

@weather_app.route('/weather', methods=['POST'])
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

    return redirect(url_for('weather_app.index_get'))

@weather_app.route('weather/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('weather_app.index_get'))