from flask import render_template, request, redirect, url_for

from . import app
from .database import  session, Entry

PAGINATE_BY = 10

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
    """start = page_index * PAGINATE_BY + 1 - Caused Entry 24 not to show on the website"""
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
def add_entry_get():
    return render_template("add_entry.html")


@app.route('/entry/add', methods=['POST'])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form['content'],
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
def edit_get(id):
    entry = session.query(Entry).get(id)

    return render_template(
        "edit_entry.html",
        entry=entry,
    )


@app.route('/entry/<int:id>/edit', methods=['POST'])
def edit_post(id):

    entry = session.query(Entry).get(id)
    entry.title = request.form['title']
    entry.content = request.form['content']

    session.commit()
    return redirect(url_for("view_entry", id=id))


@app.route('/entry/<id>/delete', methods=['GET'])
def delete_entry(id):

    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()

    return redirect(url_for("entries"))
