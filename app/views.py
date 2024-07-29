from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import eat, Exercise
from app import db
from app.forms import ExerciseForm


from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64


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


################################### Visualization #########################


@bp.route('/exercise_stats')
def exercise_stats():
    # Fetch data from the database
    daily_stats = get_exercise_stats('daily')
    weekly_stats = get_exercise_stats('weekly')
    monthly_stats = get_exercise_stats('monthly')

    # Generate charts
    daily_chart = create_bar_chart(daily_stats, 'Daily Exercise Stats')
    weekly_chart = create_bar_chart(weekly_stats, 'Weekly Exercise Stats')
    monthly_chart = create_bar_chart(monthly_stats, 'Monthly Exercise Stats')

    return render_template('exercise_stats.html', daily_chart=daily_chart, weekly_chart=weekly_chart, monthly_chart=monthly_chart)


def get_exercise_stats(period):
    now = datetime.now()

    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(weeks=4)
    else:
        return []

    stats = (Exercise.query
             .filter(Exercise.date_added >= start_date)
             .with_entities(Exercise.exercise, db.func.sum(Exercise.count).label('total_count'))
             .group_by(Exercise.exercise)
             .all())
    
    return stats


def create_bar_chart(stats, title):
    exercises = [stat.exercise for stat in stats]
    counts = [stat.total_count for stat in stats]

    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size for better spacing
    ax.bar(exercises, counts, color='skyblue')
    ax.set_title(title, color='white')
    ax.set_xlabel('Exercise', color='white')
    ax.set_ylabel('Count', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', color='white')  # Rotate x-axis labels
    fig.patch.set_facecolor('#343a40')  # Dark background color
    ax.set_facecolor('#343a40')  # Dark background color for the plot area

    # Save the chart to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor())
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return f'data:image/png;base64,{chart_data}'

