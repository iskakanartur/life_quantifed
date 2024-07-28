from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import eat, Exercise
from app import db
from app.forms import ExerciseForm

bp = Blueprint('main', __name__)

@bp.route('/')
def welcome():
    return render_template('welcome.html')

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