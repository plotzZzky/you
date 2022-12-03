from app.__init__ import app, db
from app.auth import signup_user, edit_profile
from app.models import User, Post, Image, LikePost, LikeImage, Friends, CommentPost, CommentImage
from app.src.posts import add_new_post, add_new_img, add_new_comment_image, add_new_comment_post, check_liked
from app.src.create_users import create_users, create_post, create_comments, create_likes

from flask import request, render_template, flash, redirect
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash


# # # # # # # # # # # # # # # # Importante!!!! # # # # # # # # # # # # # # # #
# Este end-point gera usuarios, postagem, comentarios e likes para a You não ficar tão vazia!
@app.route('/create', methods=['GET'])
def create():
    db.create_all()
    create_users()
    create_post()
    create_comments()
    create_likes()
    return redirect('/')


# # # # # # # # # # # # # # # # Login # # # # # # # # # # # # # # # #

@app.route('/check', methods=['GET'])
def check_login():
    if current_user.is_authenticated:
        return redirect('/profile')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Entrar")
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect('/profile')
            else:
                flash('Incorrect user or password')
                return redirect('/login')
        else:
            flash('Incorrect user or password')
            return redirect('/login')


@app.route('/signup', methods=['POST'])
def signup():
    query = signup_user(request)
    if query:
        return redirect('/notes')
    else:
        flash('Não foi possivel criar o usuario')
        return redirect('/login')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


# # # # # # # # # # # # # # # # You # # # # # # # # # # # # # # # #

@app.route('/profile', methods=['GET'])
@login_required
def show_perfil():
    posts = db.session.query(Post).filter_by(user_id=current_user.id).order_by(Post.id.desc()).all()
    check_liked(posts, current_user)
    images = db.session.query(Image).filter_by(user_id=current_user.id).order_by(Image.id.desc()).all()
    check_liked(images, current_user)
    return render_template('profile.html', user=current_user, posts=posts, images=images, title="Entrar")


# Pagina com o perfil de outros usuarios
@app.route('/profile/id=<int:user_id>', methods=['GET'])
@login_required
def show_perfil_by_id(user_id):
    if user_id == current_user.id:
        return redirect('/profile')
    user = db.session.query(User).filter_by(id=user_id).one()
    posts = db.session.query(Post).filter_by(user_id=user_id).all()
    check_liked(posts, current_user)
    images = db.session.query(Image).filter_by(user_id=user_id).all()
    check_liked(images, current_user)
    is_friend = False
    for friend in current_user.friends:
        if user.id == friend.friend_id:
            is_friend = True
    return render_template('profile.html', user=user, images=images, posts=posts, is_friend=is_friend)


@app.route('/profile/id=<int:user_id>/add', methods=['GET'])
@login_required
def add_friend(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    is_friend = False
    for friend in current_user.friends:
        if user.id == friend.friend_id:
            is_friend = True
    if is_friend:
        friend = db.session.query(Friends).filter_by(user_id=current_user.id, friend_id=user_id).one()
        db.session.delete(friend)
        db.session.commit()
    else:
        friend = Friends(user_id=current_user.id, friend_id=user_id)
        db.session.add(friend)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_perfil():
    if request.method == 'GET':
        return render_template('edit_profile.html', user=current_user, title="Profile")
    else:
        query = edit_profile(request, current_user)
        if query is True:
            flash('Alterações salvas')
            return redirect('/profile')
        else:
            flash(query)
            return render_template('edit_profile.html', user=current_user, title="Profile")


@app.route('/profile/img/add', methods=['GET', 'POST'])
@login_required
def add_img():
    if request.method == 'GET':
        return render_template('add_img.html', title="Addiconar imagem")
    else:
        add_new_img(request, current_user)
        return redirect('/profile')


@app.route('/profile/img/delete=<int:image_id>', methods=['GET'])
@login_required
def delete_img(image_id):
    image = db.session.execute(db.select(Image).filter_by(id=image_id)).scalar_one()
    db.session.delete(image)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/profile/post/add', methods=['GET', 'POST'])
@login_required
def add_said():
    if request.method == 'GET':
        return render_template('add_post.html', title="Adicionar post")
    else:
        add_new_post(request, current_user)
        return redirect('/profile')


@app.route('/profile/post/delete=<int:post_id>', methods=['GET'])
@login_required
def delete_said(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()
    if post.user.id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(request.referrer)


# # # # # # # # # # # # # # # # Horizonte # # # # # # # # # # # # # # # #

@app.route('/image/id=<int:image_id>', methods=['GET'])
@login_required
def view_image(image_id):
    image = db.session.execute(db.select(Image).filter_by(id=image_id)).one()
    check_liked(image, current_user)
    return render_template('preview_image.html', user=current_user, data=image, title="Imagem")


@app.route('/image/id=<int:image_id>/add_comment', methods=['POST'])
@login_required
def add_comment_image(image_id):
    add_new_comment_image(request, current_user, image_id)
    return redirect(request.referrer)


@app.route('/image/id=<int:image_id>/delete_comment=<int:comment_id>', methods=['GET'])
@login_required
def delete_image_comment(image_id, comment_id):
    comment = db.session.query(CommentImage).filter_by(id=comment_id, image_id=image_id).one()
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/image/id=<int:image_id>/add_like', methods=['GET'])
@login_required
def add_like_image(image_id):
    image = db.session.query(Image).filter_by(id=image_id).one()
    for item in image.likes:
        if current_user.id == item.user_id:
            like = db.session.query(LikeImage).filter_by(image_id=image_id, user_id=current_user.id).one()
            db.session.delete(like)
            db.session.commit()
            return redirect(request.referrer)
    like = LikeImage(user_id=current_user.id, image_id=image_id)
    db.session.add(like)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/post/id=<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    post = db.session.execute(db.select(Post).filter_by(id=post_id)).one()
    check_liked(post, current_user)
    return render_template('preview_post.html', user=current_user, data=post, title="Post")


@app.route('/post/id=<int:post_id>/add_comment', methods=['POST'])
@login_required
def add_comment_post(post_id):
    add_new_comment_post(request, current_user, post_id)
    return redirect(request.referrer)


@app.route('/post/id=<int:post_id>/delete_comment=<int:comment_id>', methods=['GET'])
@login_required
def delete_post_comment(post_id, comment_id):
    comment = db.session.query(CommentPost).filter_by(id=comment_id, post_id=post_id).one()
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/post/id=<int:post_id>/add_like', methods=['GET'])
@login_required
def add_like_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()
    for item in post.likes:
        if current_user.id == item.user_id:
            like = db.session.query(LikePost).filter_by(post_id=post_id, user_id=current_user.id).one()
            db.session.delete(like)
            db.session.commit()
            return redirect(request.referrer)
    like = LikePost(user_id=current_user.id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/friends/post', methods=['GET'])
@login_required
def friends_posts():
    friends = []
    for friend in current_user.friends:
        friends.append(friend.friend_id)
    data = db.session.query(Post).filter(Post.user_id.in_(friends)).all()
    check_liked(data, current_user)
    empty_text = "Você ainda não segue ninguem!"
    return render_template('posts.html', user=current_user, data=data, title="Posts", empty_text=empty_text)


@app.route('/friends/img', methods=['GET'])
@login_required
def friends_images():
    friends = []
    for friend in current_user.friends:
        friends.append(friend.friend_id)
    data = db.session.query(Image).filter(Image.user_id.in_(friends)).order_by(Image.id.desc()).all()
    check_liked(data, current_user)
    empty_text = "Você ainda não segue ninguem!"
    return render_template('images.html', user=current_user, data=data, title="Imagens", empty_text=empty_text)


@app.route('/friends/find', methods=['GET'])
@login_required
def find_friends():
    data = []
    for friend in current_user.friends:
        data.append(friend.friend_id)
    friends = db.session.query(User).filter(User.id.in_(data)).all()
    users = db.session.query(User).filter(User.id.notin_(data)).filter(User.id != current_user.id).all()
    return render_template('users.html', users=users, friends=friends, title="Buscar amigos")


@app.route('/all/post', methods=['GET'])
@login_required
def all_posts():
    query = db.session.query(Post).order_by(Post.id.desc()).all()
    check_liked(query, current_user)
    empty_text = "Ainda não há nada por aqui!"
    return render_template('posts.html', user=current_user, data=query, title="Posts", empty_text=empty_text)


@app.route('/all/img', methods=['GET'])
@login_required
def all_img():
    query = db.session.query(Image).order_by(Image.id.desc()).all()
    check_liked(query, current_user)
    empty_text = "Ainda não há nada por aqui!"
    return render_template('images.html', user=current_user, data=query, title="Imagens", empty_text=empty_text)


# # # # # # # # # # # # # # # # Gerais # # # # # # # # # # # # # # # #

@app.route('/', methods=['GET'])
def show_home():
    return render_template('home.html', title="Inicio")


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="Sobre")


@app.errorhandler(404)
@app.errorhandler(405)
def not_found(e):
    flash('Pagina não encontrada! tente novamente mais tarde')
    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect('/')
