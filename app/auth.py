from app.__init__ import db, app
from app.models import User

from werkzeug.security import generate_password_hash
from flask_login import login_user
from werkzeug.utils import secure_filename
from pathlib import Path
import os


def create_username(request):
    username = request.form['username']
    if len(username) > 3:
        return username
    else:
        return None


def create_password(request, min_password):
    password = request.form['password']
    pwd = request.form['pwd']
    if password == pwd and len(password) > min_password:
        result = generate_password_hash(password)
        return result
    else:
        return None


def create_email(request):
    email = request.form['email']
    if '@' in email and len(email) > 11:
        return email
    else:
        return None


def update_username(request, user):
    new_username = request.form['username']
    if new_username != user.username and new_username != '':
        if len(new_username) > 3:
            user.username = new_username
            db.session.commit()
            return True
        else:
            return 'O username de ter no minimo 3 caracteres'
    return True


def update_email(request, user):
    email = request.form['email']
    if email != user.email:
        if '@' in email and len(email) >= 10:
            user.email = email
            db.session.commit()
            return True
        else:
            return 'Email invalido'
    return True


def update_password(request, user, min_pwd):
    passwd = request.form['password']
    print(passwd)
    pwd = request.form['pwd']
    if passwd != '' and pwd != '':
        if passwd == pwd:
            if len(passwd) >= min_pwd:
                password = generate_password_hash(passwd)
                user.password = password
                db.session.commit()
                return True
            else:
                return 'A Senha precisa ter no minimo 3 caracteres'
        else:
            return 'As senhas precisam ser iguais'
    return True


def update_picture(request, user):
    picture = request.files['picture']
    if picture.filename != '':
        pic = save_profile_picture(picture, user, user.id)
        user.picture = pic
        db.session.commit()
        return True


def update_banner(request, user):
    banner = request.files['banner']
    if banner.filename != '':
        pic = save_profile_picture(banner, user, 'banner')
        user.banner = pic
        db.session.commit()
        return True


def signup_user(request):
    username = create_username(request)
    email = create_email(request)
    password = create_password(request, 3)
    if username and email and password is not None:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return True
    else:
        return False


def edit_profile(request, user):
    user = db.session.query(User).filter_by(id=user.id).one()
    print(user)
    password = update_password(request, user, 3)
    if password is not True:
        return password
    username = update_username(request, user)
    if username is not True:
        return username
    email = update_email(request, user)
    if email is not True:
        return email
    update_picture(request, user)
    update_banner(request, user)
    user.status = request.form['status']
    db.session.commit()
    return True


def save_profile_picture(picture, user, name_file):
    post_path = f"{app.config['UPLOAD_FOLDER']}/profiles"
    path = Path(f"{post_path}/{user.id}")
    path.mkdir(parents=True, exist_ok=True)
    ext = picture.filename.split('.')[1]
    name = f"{name_file}.{ext}"
    filename = secure_filename(name)
    picture.save(os.path.join(path, filename))
    return f"/uploaded_files/profiles/{user.id}/{name}"
