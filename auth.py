from app import db, User
from werkzeug.security import generate_password_hash
from flask_login import login_user
from werkzeug.utils import secure_filename
from pathlib import Path
from app import app
import os


def create_username(username):
    if len(username) > 3:
        return username
    else:
        return None


def create_password(password, password_b, min_password):
    if password == password_b and len(password) > min_password:
        return password
    else:
        return None


def create_email(email):
    if '@' in email and len(email) > 11:
        return email
    else:
        return None


def update_username(username, user_id):
    user = User.query.filter_by(id=user_id).first()
    user.username = username
    db.session.commit()


def update_email(email, user_id):
    if '@' in email and len(email) >= 10:
        user = User.query.filter_by(id=user_id).first()
        user.email = email
        db.session.commit()


def update_password(password, user_id):
    if len(password) >= 4:
        user = User.query.filter_by(id=user_id).first()
        user.email = generate_password_hash(password)
        db.session.commit()


def signup_user(request):
    f_name = request.form['username']
    f_email = request.form['email']
    pwd = request.form['password']
    pwd_2 = request.form['pwd']
    username = create_username(f_name)
    email = create_email(f_email)
    passwd = create_password(pwd, pwd_2, 2)
    if username and email and passwd is not None:
        password = generate_password_hash(passwd)
        user = User(username=username, email=email, password=password)  # type: ignore
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return True
    else:
        return False


def edit_profile(request, user):
    username = request.form['username']
    picture = request.files['picture']
    banner = request.files['banner']
    status = request.form['status']
    user = db.session.execute(db.select(User).filter_by(id=user.id)).scalar_one()
    password = check_password(request, user)
    if password is False:
        return False
    email = request.form['email']
    user.username = username
    change_picture(picture, user)
    change_banner(banner, user)
    user.email = email
    user.status = status
    db.session.commit()
    return True


def check_password(request, user):
    passwd = request.form['password']
    pwd = request.form['pwd']
    if passwd == pwd:
        if passwd == '' or pwd == '':
            return None
        else:
            password = generate_password_hash(passwd)
            user.password = password
    else:
        return False


def change_picture(picture, user):
    if picture.filename != '':
        pic = save_profile_picture(picture, user, user.id)
        user.picture = pic


def change_banner(banner, user):
    print(banner)
    if banner.filename != '':
        pic = save_profile_picture(banner, user, 'banner')
        user.banner = pic


def save_profile_picture(picture, user, name_file):
    post_path = f"{app.config['UPLOAD_FOLDER']}/profiles"
    path = Path(f"{post_path}/{user.id}")
    path.mkdir(parents=True, exist_ok=True)
    ext = picture.filename.split('.')[1]
    name = f"{name_file}.{ext}"
    filename = secure_filename(name)
    picture.save(os.path.join(path, filename))
    return f"/uploaded_files/profiles/{user.id}/{name}"
