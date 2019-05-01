from flask import Flask, request, render_template, redirect, session, flash
from jinja2 import StrictUndefined
import word_guess_web_app
from word_guess_web_app import LetterRound
app = Flask(__name__)
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def main_page():
    """Homepage"""

    return render_template('main_page.html')


@app.route('/explain_game', methods=['POST'])
def explain_game():
    """Explain game and ask user to choose first letter"""

    player_name = request.form.get('player_name')

    #word = word_guess_web_app.get_word_from_api()
    word = word_guess_web_app.get_local_word()


    session['player_name'] = player_name
    session['word'] = word
    session['remaining_guesses'] = 6


    return render_template('explain_game.html', player_name=player_name, remaining_guesses=session['remaining_guesses'])


@app.route('/choose_letter', methods=['POST'])
def choose_letter():
    """Ask user to choose a letter"""

    letter = request.form.get('letter')
    player_name = session['player_name']
    word = session['word']
    print(type(word))
    remaining_guesses = session['remaining_guesses'] - 1
    session['remaining_guesses'] = remaining_guesses
    session['wrong_guesses'] = []
    session['right_guesses'] = []

    letter_round = LetterRound(word)
    if letter_round.validate_input(letter):
        is_letter_in_word = letter_round.is_letter_in_word(letter, player_name)
        if is_letter_in_word == True:
            session['right_guesses'].append(letter)
            message = 'Awesome job, {}! This letter is in the word:  {}'.format(player_name, letter)
        else:
            session['wrong_guesses'].append(letter)

            message = 'Sorry, {}! This letter is not in the word:  {}'.format(player_name, letter)
    else:
        message = 'Please enter a valid input'


    return render_template('choose_letter.html', remaining_guesses=remaining_guesses, message=message, wrong_guesses=session['wrong_guesses'], right_guesses=session['right_guesses'])


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()  # the app.run should be the last thing on your app in order to not cause conflicts
