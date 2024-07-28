from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import eat, Exercise
from app import db
from app.forms import ExerciseForm
import datetime
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
def welcome():
    return render_template('index.html')

@bp.route('/eat')
def view_eat():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    eats = eat.query.order_by(eat.date_added.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', eats=eats)

@bp.route('/exercise', methods=['GET', 'POST'])
def view_exercise():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = Exercise(exercise=form.exercise.data, count=form.count.data, comment=form.comment.data)
        db.session.add(exercise)
        db.session.commit()
        return redirect(url_for('main.view_exercise'))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    exercises = Exercise.query.order_by(Exercise.date_added.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('exercise.html', exercises=exercises, form=form)

@bp.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = Exercise(exercise=form.exercise.data, count=form.count.data, comment=form.comment.data)
        db.session.add(exercise)
        db.session.commit()
        flash('Exercise added successfully', 'success')
        return redirect(url_for('main.view_exercise'))
    return render_template('add_exercise.html', form=form)

@bp.route('/delete_exercise/<int:id>', methods=['POST'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    flash('Exercise deleted successfully', 'success')
    return redirect(url_for('main.view_exercise'))

@bp.route('/exercise_data')
def exercise_data():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    daily_stats = db.session.query(
        Exercise.exercise,
        func.sum(Exercise.count).label('total_count')
    ).filter(
        func.date(Exercise.date_added) == today
    ).group_by(Exercise.exercise).all()

    daily_stats_dict = {exercise: count for exercise, count in daily_stats}

    weekly_stats = db.session.query(
        Exercise.exercise,
        func.sum(Exercise.count).label('total_count')
    ).filter(
        Exercise.date_added >= start_of_week
    ).group_by(Exercise.exercise).all()

    weekly_stats_dict = {exercise: count for exercise, count in weekly_stats}

    monthly_stats = db.session.query(
        Exercise.exercise,
        func.sum(Exercise.count).label('total_count')
    ).filter(
        Exercise.date_added >= start_of_month
    ).group_by(Exercise.exercise).all()

    monthly_stats_dict = {exercise: count for exercise, count in monthly_stats}

    # Debug print statements
    print("Daily Stats:", daily_stats_dict)
    print("Weekly Stats:", weekly_stats_dict)
    print("Monthly Stats:", monthly_stats_dict)

    return jsonify({
        'daily_stats': daily_stats_dict,
        'weekly_stats': weekly_stats_dict,
        'monthly_stats': monthly_stats_dict
    })
