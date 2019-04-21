from flask import Flask, request, render_template, redirect, session, flash
from jinja2 import StrictUndefined
app = Flask(__name__)
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')

def main_page():
    """Homepage"""

    return render_template('main_page.html')

@app.route('/choose_letter')
def choose_letter():
    """Ask user to choose a letter"""

    player_name = request.form.get('player_name')

    return render_template('choose_letter.html', player_name = player_name)

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()  # the app.run should be the last thing on your app in order to not cause conflicts
