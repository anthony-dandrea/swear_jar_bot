import os
import sqlite3

from random import choice

from flask import Flask, render_template, request, g, session, redirect, url_for
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'test_sinners.db'), # TODO <--- DB name?
    DEBUG=True,
    SECRET_KEY='development key', # Do we care?
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True) # TODO <-- we care?

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

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

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
@app.route('/', methods=['GET', 'POST'])
def index():
    # here we want to get the value of user (i.e. ?user=some-value)
    form = NameForm()
    if form.validate_on_submit():
        user = form.name.data

        if user:
            print('User found: {}'.format(user))
            db = get_db()
            # Placeholder SQL statement because I don't know shit
            cur = db.execute('SELECT swear_comment FROM comments WHERE user = "{}" AND paid = 0'.format(user))
            session['comments'] = [comment[0] for comment in cur.fetchall()]
            print('Comments found under user:')
            for comment in session['comments']:
                print('{}'.format(comment))
        else:
            print('No user found')
            session['comments'] = []
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template('index.html', form=form, user=session.get('name'), comments=session.get('comments'))

@app.route('/user/<user>')
def redirect_with_user(user):
    # show the user profile for that user
    session['name'] = user
    session['comments'] = get_comments(user)
    return redirect(url_for('index'))

@app.route('/random')
def redirect_with_random_user():
    db = get_db()
    # Placeholder SQL statement because I don't know shit
    cur = db.execute('SELECT user FROM comments')
    user = choice(cur.fetchall())[0]
    session['name'] = user
    session['comments'] = get_comments(user)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
