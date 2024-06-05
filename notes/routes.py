from flask import render_template, redirect, url_for, request, g, abort, flash
from . import app, db, NotesModel, CategoryModel, User, bcrypt, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user


@app.route('/', methods=['GET', 'POST'])
def home():

    # creating new notes/task
    if request.method == 'POST':
        title = request.form.get('title')
        category_name = request.form.get('category')

        existing_category = CategoryModel.query.filter_by(title=category_name).first()

        if existing_category:
            # Use the existing category
            category = existing_category
        else:
            # Create a new category
            category = CategoryModel(title=category_name)
            category.save()

        notes = NotesModel(title=title, category=category)
        notes.save()
        return redirect('/')
    
    notes = NotesModel.query.filter_by(user_id=current_user.id)
    category = CategoryModel.query.all()
    return render_template('home/home.html', notes=notes, categories=category, user=current_user)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        category_name = request.form.get('category')
        
        existing_category = CategoryModel.query.filter_by(user_id=current_user.id, title=category_name).first()

        if existing_category:
            # Use the existing category
            category = existing_category
        else:
            # Create a new category
            category = CategoryModel(title=category_name)
            category.save()

        notes = NotesModel(title=title, category=category)
        notes.save()
        # request.ho
        print(g, request.headers)
        return redirect('/')
    return render_template('add_note.html')

@app.route('/update/note/<int:pk>', methods=['GET', 'POST'])
def update_note(pk):
    note = NotesModel.query.get_or_404(pk)
    if not note:
        abort(404)
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.status = request.form.get('status')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update_note.html', note=note) 


@app.route('/delete/note/<int:pk>', methods=['GET', 'POST'])
def delete_note(pk):
    note = NotesModel.query.get_or_404(pk)
        # return redirect()
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error = 'Invalid Credentials'
            return render_template('register.html', error=error)
        user = User(username=username, password=password)
        user.save()
        flash(f'{username} succesfully registered')
        return redirect(url_for('home'))
    return render_template('register.html')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('User logged in succesfully')
                return redirect(url_for('home'))
            else:
                return render_template('login.html', errors='Invalid Credentials') 
    return render_template('login.html', errors='Invalid Credentials') 
    