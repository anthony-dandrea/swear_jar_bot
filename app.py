import os
from flask import Flask, render_template
from flask.ext import assets

app = Flask(__name__)

env = assets.Environment(app)

# Tell Flask where to look for assets
env.load_path = [
    os.path.join(os.path.dirname(__file__), 'assets/bower_components'),
    os.path.join(os.path.dirname(__file__), 'assets/fonts'),
    os.path.join(os.path.dirname(__file__), 'assets/stylesheets'),
    os.path.join(os.path.dirname(__file__), 'assets/scripts'),
]

env.register (
    'css_all',
    assets.Bundle(
        'main.scss',
        filters='sass',
        output='css_all.css'
    )
)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
