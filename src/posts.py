from datetime import datetime
from app import db, Post, Image, app, CommentPost, CommentImage
from werkzeug.utils import secure_filename
import os


def add_new_post(request, user):
    text = request.form['text']
    user_id = user.id
    date = datetime.today().strftime('%d/%m/%Y')
    post = Post(user_id=user_id, text=text, date=date, comments=[])
    db.session.add(post)
    db.session.commit()
    return post


def add_new_img(request, user):
    text = request.form['text-image']
    user_id = user.id
    date = datetime.today().strftime('%d/%m/%Y')
    image = request.files['image']
    picture = upload_image(image)
    image = Image(user_id=user_id, date=date, text=text, img_path=picture, comments=[])
    db.session.add(image)
    db.session.commit()


def add_new_comment_image(request, user, image_id):
    comment = request.form['comment']
    date = datetime.today().strftime('%d/%m/%Y')
    query = CommentImage(text=comment, date=date, user_id=user.id, image_id=image_id)
    db.session.add(query)
    db.session.commit()


def add_new_comment_post(request, user, post_id):
    comment = request.form['comment']
    date = datetime.today().strftime('%d/%m/%Y')
    query = CommentPost(text=comment, date=date, user_id=user.id, post_id=post_id)
    db.session.add(query)
    db.session.commit()


def upload_image(file):
    query = db.session.query(Image).order_by(Image.id.desc()).first()
    if query is None:
        n = 1
    else:
        n = query.id + 1
    post_path = f"{app.config['UPLOAD_FOLDER']}/images"
    ext = file.filename.split('.')[1]
    name = f"{n}.{ext}"
    filename = secure_filename(name)
    file.save(os.path.join(post_path, filename))
    return f"/uploaded_files/images/{name}"


def check_liked(query, user):
    for post in query:
        post.liked = False
        for like in post.likes:
            if like.user_id == user.id:
                post.liked = True
