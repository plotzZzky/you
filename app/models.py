from app.__init__ import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(96), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(96), unique=True)
    picture = db.Column(db.Text())
    status = db.Column(db.Text())
    banner = db.Column(db.Text())
    friends = db.relationship('Friends', backref='user', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.status = "Olá, sou novo na You!!!"
        self.picture = "/uploaded_files/profile.jpeg"
        self.banner = "/uploaded_files/banner.jpg"


class Friends(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer())


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
    text = db.Column(db.Text())
    date = db.Column(db.Date())
    comments = db.relationship('CommentPost', backref='post', lazy=True)
    likes = db.relationship('LikePost', backref='post', lazy=True)
    liked = db.Column(db.Boolean())


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
    text = db.Column(db.Text())
    img_path = db.Column(db.Text())
    date = db.Column(db.Date())
    comments = db.relationship('CommentImage', backref='images', lazy=True)
    likes = db.relationship('LikeImage', backref='image', lazy=True)
    liked = db.Column(db.Boolean())


class CommentPost(db.Model):
    __tablename__ = 'comments_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())


class CommentImage(db.Model):
    __tablename__ = 'comments_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())


class LikePost(db.Model):
    __tabele__ = 'likeposts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)


class LikeImage(db.Model):
    __tabele__ = 'likeimages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
