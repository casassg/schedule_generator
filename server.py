# all the imports
import psycopg2
from psycopg2 import extras
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import config
from contextlib import closing
from database import connect_db



# create our little application :)

app = Flask(__name__)
app.config.from_object(config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as file:
            db.cursor().execute(file.read())
        db.commit()


def add_paprika():
    with closing(connect_db()) as db:
        db.execute('UPDATE entries set title = ?', ['PAPRIKA'])
        db.commit()


def query_db(query, args=(), one=False):
    dict_cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(query, args)
    rv = dict_cur.fetchall()
    dict_cur.close()
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    entries = query_db('select title, text from entries order by id desc')
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    dict_cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    dict_cur.execute('insert into entries (title, text) values (%s,%s)', [request.form['title'], request.form['text']])
    dict_cur.execute('COMMIT')
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
