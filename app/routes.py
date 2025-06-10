from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import TaskForm, NoteForm  # <-- import NoteForm as well
from app import db
from app.models import Task, Note     # <-- import Note model
from app import csrf  # import csrf for awareness, no need to decorate

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, tasks=tasks)

@main.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            completed=form.completed.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_task.html', user=current_user, form=form)

@main.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.completed = form.completed.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('edit_task.html', user=current_user, form=form, task=task)

@main.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# --- NOTE TAKING ROUTES START HERE ---

@main.route('/notes')
@login_required
def notes():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.timestamp.desc()).all()
    return render_template('notes.html', notes=notes, user=current_user)

@main.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(content=form.content.data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added successfully!', 'success')
        return redirect(url_for('main.notes'))
    return render_template('add_note.html', form=form, user=current_user)

@main.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.content = form.content.data
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('main.notes'))
    return render_template('edit_note.html', form=form, user=current_user)

@main.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'success')
    return redirect(url_for('main.notes'))
