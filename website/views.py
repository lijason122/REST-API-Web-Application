from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
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