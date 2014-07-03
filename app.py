import os
import sqlite3
from flask import Flask, render_template, request, g

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

@app.route('/')
def index():
    # here we want to get the value of user (i.e. ?user=some-value)
    user = request.args.get('user', None)

    if user:
        print('User found: {}'.format(user))
        db = get_db()
        # Placeholder SQL statement because I don't know shit
        cur = db.execute('SELECT swear_comment FROM comments WHERE user = "{}" AND paid = 0'.format(user))
        comments = [comment[0] for comment in cur.fetchall()]
        print('Comments found under user:')
        for comment in comments:
            print('{}'.format(comment))
    else:
        print('No user found')
        comments = []

    return render_template('index.html', user=user, comments=comments)

# TODO: If we want to add_comment api shit, we can do that here
#@app.route('/add_comment', methods=['POST'])
#def add_comment_api():
#    # TODO add some authentication that only swearbot knows about
#    db = get_db()
#    db.execute('INSERT INTO comments (user, comment) VALUES (?, ?)',
#                    [user???, comment???]) # <-- figure out request format
#    db.commit()
#    # TODO return some json response to the bot?


if __name__ == '__main__':
    app.run()
