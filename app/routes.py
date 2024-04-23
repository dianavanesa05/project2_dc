from flask import render_template, flash, redirect, url_for, request, Flask
from flask.wrappers import Response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import urls
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import CommentsForm, LoginForm, ProfileForm, RegistrationForm, CommentsOtherProfileForm
from app.models import Comments, User, Img
import os
import uuid
from datetime import datetime

@app.route('/')
@app.route('/home')
def home():
    logout_user()
    return render_template('home.html')


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = ProfileForm()
    if request.method == "POST":
        user = User.query.filter_by(username=current_user.username).first()
        user.fName = form.fName.data
        user.lName = form.lName.data
        user.year = form.year.data
        user.major = form.major.data
        pic = request.files['pic']
        
        # Generate a unique filename
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}_{secure_filename(pic.filename)}"
        mimetype = pic.mimetype
        img = Img(img=pic.read(), mimetype=mimetype, name=filename, username=current_user.username)
        
        # Check if the user already has an image, delete it if exists
        existing_img = Img.query.filter_by(username=current_user.username).first()
        if existing_img:
            db.session.delete(existing_img)

        db.session.add(img)
        db.session.commit()
        return redirect('/index')

    if current_user.fName is not None:
        form.fName.data = current_user.fName
        form.lName.data = current_user.lName
        form.year.data = current_user.year 
        form.major.data = current_user.major

    return render_template('edit.html', form=form)


@app.route('/pic')
def get_img():
    img = Img.query.filter_by(username=current_user.username).first()
    if not img:
        return render_template('noPic.html')
    return Response(img.img, mimetype=img.mimetype)

@app.route('/otherPic/<int:uid>')
def get_other_img(uid):
    user = User.query.filter_by(id=uid).first()
    img = Img.query.filter_by(username=user.username).first()
    if not img:
        return render_template('noPic.html')
    return Response(img.img, mimetype=img.mimetype)

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CommentsForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        comment = Comments(username=current_user.username, comments=form.comments.data, profile_id=user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect('/index')
    return render_template('index.html', title='Home', form=form)

@app.route('/delete/<int:cid>')
def deleteProfileComment(cid):
    Comments.query.filter_by(id=cid).delete()
    db.session.commit()
    return redirect('/index')

@app.route('/deleteOther/<int:cid>/<int:uid>')
def deleteOtherProfileComment(cid, uid):
    Comments.query.filter_by(id=cid).delete()
    db.session.commit()
    return redirect('/users/' + str(uid))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/finder')
def finder():
    users = User.query.filter(User.username!=current_user.username).all()
    has_users = bool(users)
    userMajor = User.query.filter_by(major=current_user.major).filter(User.username!=current_user.username).all()
    has_major = bool(userMajor)
    userClass = User.query.filter_by(year=current_user.year).filter(User.username!=current_user.username).all()
    has_class = bool(userClass)
    usersMajorAndClass = User.query.filter_by(major=current_user.major, year=current_user.year).filter(User.username!=current_user.username).all()
    has_major_class = bool(usersMajorAndClass)
    return render_template('finder.html', users=users, userMajor=userMajor, userClass=userClass, has_major=has_major, has_class=has_class, has_users=has_users, usersMajorAndClass=usersMajorAndClass, has_major_class=has_major_class)

@app.route('/users/<int:uid>', methods=['GET', 'POST'])
def generalProfile(uid):
    form = CommentsOtherProfileForm()
    user = User.query.filter_by(id=uid).first()
    if form.validate_on_submit():
        comment = Comments(username=current_user.username, comments=form.comments.data, profile_id=user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect('/users/' + str(uid))
    return render_template('profile.html', user=user, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
