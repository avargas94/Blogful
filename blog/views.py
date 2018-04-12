from flask import render_template, request, redirect, url_for

from . import app
from .database import  session, Entry

from flask import flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from .database import User


@app.route('/', methods=['GET'])
@app.route('/page/<int:page>', methods=['GET'])
def entries(page=1):

    page_index = page - 1
    limit = 10
    requested_limit = request.args.get('limit')

    if requested_limit is not None:
        limit = int(requested_limit)

    count = session.query(Entry).count()

    start = page_index * limit
    end = start + limit

    total_pages = (count - 1) // limit + 1
    has_next = page_index < total_pages -1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    return render_template(
        "entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )


@app.route('/entry/add', methods=['GET'])
@login_required
def add_entry_get():
    return render_template("add_entry.html")


@app.route('/entry/add', methods=['POST'])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form['content'],
        author=current_user,
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))


@app.route('/entry/<int:id>')
def view_entry(id):
    id = id
    entry = session.query(Entry).get(id)

    return render_template(
        "view_entry.html",
        entry=entry,
    )


@app.route('/entry/<int:id>/edit', methods=['GET'])
@login_required
def edit_get(id):
    entry = session.query(Entry).get(id)

    return render_template(
        "edit_entry.html",
        entry=entry,
    )


@app.route('/entry/<int:id>/edit', methods=['POST'])
@login_required
def edit_post(id):

    entry = session.query(Entry).get(id)
    entry.title = request.form['title']
    entry.content = request.form['content']

    session.commit()
    return redirect(url_for("view_entry", id=id))


@app.route('/entry/<id>/delete', methods=['GET'])
@login_required
def delete_entry(id):

    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()

    return redirect(url_for("entries"))


@app.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))


@app.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('entries'))