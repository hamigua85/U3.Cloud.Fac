from flask import render_template, redirect, url_for, abort, flash, request, jsonify, current_app
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from app.models import db
from app.models import User, Role, Post, File, Task
from flask_login import login_required, current_user
from ..decorators import admin_required
from ..models import Permission
from werkzeug.utils import secure_filename
import datetime, sqlite3, time
import uuid
from app import task_scheduler, redis


ALLOWED_EXTENSIONS = set(['gcode'])


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def query_uploaded_files():
    files = File.query.filter_by(owner_id=current_user._get_current_object().id).all()
    index = 0
    file_list = []
    for uploaded_file in files:
        index += 1
        temp = File.data_parser(index, uploaded_file)
        file_list.append(temp)
    return file_list


@main.route('/uploaded-files')
@login_required
def uploaded_files():
    file_list = query_uploaded_files()
    return jsonify(file_list)


@main.route('/delete-files')
@login_required
def delete_files():
    filesname = request.args.get('files').split(',')
    for filename in filesname:
        file = File.query.filter_by(name=filename).first()
        db.session.delete(file)
    file_list = query_uploaded_files()
    return jsonify(file_list)


@main.route('/print-files')
@login_required
def print_files():
    filesname = request.args.get('files').split(',')
    for filename in filesname:
        file = File.query.filter_by(name=filename).first()
        new_task = Task(file_name=file.name,
                        uuid=str(uuid.uuid1()),
                        start_time=datetime.datetime.now(),
                        progress=0,
                        owner=current_user._get_current_object(),
                        priority=1,
                        state='waiting')
        db.session.add(new_task)
    return jsonify()


@main.route('/tasks-info')
@login_required
def task_info():
    task_waiting = Task.query.filter_by(state='waiting').all()
    task_printing = Task.query.filter_by(state='printing').all()
    index = 0
    task_waiting_list = []
    task_printing_list = []
    for task_wait in task_waiting:
        index += 1
        temp = Task.data_parser('waiting', index, task_wait)
        task_waiting_list.append(temp)
    index = 0
    for task_print in task_printing:
        index += 1
        temp = Task.data_parser('printing', index, task_print)
        task_printing_list.append(temp)
    return jsonify(task_waiting_list=task_waiting_list, task_printing_list=task_printing_list)


@main.route('/task', methods=['GET', 'POST'])
@login_required
@admin_required
def task():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        try:
            uploaded_files = request.files.getlist('file')
            print('get files')
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    str = file.stream.read()
                    size = len(str)
                    temp = File(name=time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + '_' + filename,
                                content=sqlite3.Binary(str),
                                size=size,
                                owner=current_user._get_current_object())
                    db.session.add(temp)
        except Exception, e:
            print(e)
        return redirect(url_for('main.task'))
    return render_template('tasks.html')


@main.route('/online-machines', methods=['GET', 'POST'])
@login_required
@admin_required
def online_machines():
    if request.method == 'GET':
        cmd = request.args.get('cmd')
        if cmd == 'machine_info':
            machines_info = task_scheduler.update_online_machines()
            return jsonify(machines_info)
    return render_template('online_machines.html')


@main.route('/online_machine_state', methods=['POST'])
def online_machine_state():
    if request.method == 'POST':
        redis.set('{0} : {1}'.format(request.headers.environ['REMOTE_ADDR'], request.headers.environ['REMOTE_PORT']),
                  request.data, 5)
        return jsonify()

