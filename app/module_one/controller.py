import os
import sqlite3
import praw

from app import app

from random import choice

from flask import Blueprint, Flask, render_template, request, g, session, redirect, url_for
from flask.ext.wtf import Form
from flask.ext import assets

from wtforms import StringField, SubmitField
from wtforms.validators import Required

module_one = Blueprint('swear_routes', __name__, template_folder='templates')

########
# DB connection, initialization, and closing functions
########
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE']) # Note DATABASE config attr, above
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def get_comments(user):
    db = get_db()
    # Placeholder SQL statement because I don't know shit
    cur = db.execute('SELECT swear_comment FROM comments WHERE user = "{}" AND paid = 0'.format(user))
    return [comment[0] for comment in cur.fetchall()]

########
# Forms
########
class NameForm(Form):
    name = StringField('What yo name?', validators=[Required()])
    submit = SubmitField('Submit')

class SwearJarForm(Form):
    cc_num = StringField('What yo name?', validators=[Required()])
    cc_exp = StringField('What yo name?', validators=[Required()])

########
# Routes
########
@module_one.route('/', methods=['GET', 'POST'])
def index():
    # here we want to get the value of user (i.e. ?user=some-value)
    form = NameForm()
    if form.validate_on_submit():
        user = form.name.data
        print('User found: {}'.format(user))

        session['comments'] = get_comments(user)
        print('Comments found under user:')
        for comment in session['comments']:
            print('{}'.format(comment))
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template('index.html', form=form, user=session.get('name'), comments=session.get('comments'))

@module_one.route('/user/<user>')
def redirect_with_user(user):
    # show the user profile for that user
    session['name'] = user
    session['comments'] = get_comments(user)
    return redirect(url_for('index'))

@module_one.route('/random')
def redirect_with_random_user():
    db = get_db()
    # Placeholder SQL statement because I don't know shit
    cur = db.execute('SELECT user FROM comments')
    user = choice(cur.fetchall())[0]
    session['name'] = user
    session['comments'] = get_comments(user)
    return redirect(url_for('swear_routes.index'))
