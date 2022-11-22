from app import User, db, Post, CommentPost, LikePost
from werkzeug.security import generate_password_hash
from datetime import datetime


def create_users():
    password = generate_password_hash('123')
    user = User(username='pedrinho', password=password, email='pedrinho@mail.com')
    db.session.add(user)
    db.session.commit()
    user = User(username='bruce', password=password, email=' wayne@mail.com')
    db.session.add(user)
    db.session.commit()
    user = User(username='michael', password=password, email='sr.jackson@mail.com')
    db.session.add(user)
    db.session.commit()
    user = User(username='marilyn', password=password, email='monroe.marilyn@mail.com')
    db.session.add(user)
    db.session.commit()


def create_post():
    date = datetime.today().strftime('%d/%m/%Y')
    post = Post(user_id=2, text="Eu não sou o Batman!!", date=date)
    db.session.add(post)
    db.session.commit()
    post = Post(user_id=1, text="Que dia mais quente!!!", date=date)
    db.session.add(post)
    db.session.commit()
    post = Post(user_id=3, text="Thriller night!! There ain't no second chance...", date=date)
    db.session.add(post)
    db.session.commit()


def create_comments():
    date = datetime.today().strftime('%d/%m/%Y')
    comment = CommentPost(user_id=4, post_id=2, text='Quente sou eu!', date=date)
    db.session.add(comment)
    db.session.commit()
    comment = CommentPost(user_id=1, post_id=3, text='Curti essa musica S2', date=date)
    db.session.add(comment)
    db.session.commit()
    comment = CommentPost(user_id=1, post_id=1, text='Todos sabemos que não..', date=date)
    db.session.add(comment)
    db.session.commit()


def create_likes():
    like = LikePost(user_id=1, post_id=1)
    db.session.add(like)
    db.session.commit()
    like = LikePost(user_id=1, post_id=1)
    db.session.add(like)
    db.session.commit()
    like = LikePost(user_id=2, post_id=3)
    db.session.add(like)
    db.session.commit()
    like = LikePost(user_id=4, post_id=2)
    db.session.add(like)
    db.session.commit()
