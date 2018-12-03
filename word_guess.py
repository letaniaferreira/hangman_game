import random
import requests

word = ''
size = len(word)

wrong_guesses = []
right_guesses = [''] * size
show_guesses = ''


def get_word_from_api():
    """
    Calls api and gets random word.
    :return: Word chosen by computer to play game
    """
    words_response = requests.get('http://app.linkedin-reach.io/words')
    if words_response.ok:
        words_string = words_response.text

    else:
        print('api call not successful')

    words = words_string.split('\n')
    word = random.choice(words)
    return word

#delete this
def get_local_word():
    words = ['house', 'casa']
    word = random.choice(words)
    return word


def validate_input(letter):
    """
    Verifies validity of user input.

    :param letter: User guess
    :return: Boolean
    >>> validate_input('abc')
    Please enter a single letter
    <BLANKLINE>
    False
    >>> validate_input('abc123')
    Please enter a letter
    <BLANKLINE>
    False
    >>> validate_input('a')
    True
    >>> validate_input('3')
    Please enter a letter
    <BLANKLINE>
    False
    >>> validate_input('')
    Please enter a letter
    <BLANKLINE>
    False
    """

    if not letter.isalpha():
        print('Please enter a letter\n')
    elif len(letter) != 1:
        print('Please enter a single letter\n')
    elif letter in wrong_guesses:
        print('You already tried this letter. Try a different one\n')
    else:
        return True
    return False


def print_word(right_guesses, show_guesses):
    """
    Prints the portions of the word that have been guessed and a list of letters
    which were guessed that are not in the word.

    :param right_guesses: list with as many empty elements as the size of the word to be guessed
    :param show_guesses: string showing the location of the correct guesses
    """

    for letter in right_guesses:
        if letter == '':
            letter = '_'
        show_guesses += (letter + ' ')
    print(show_guesses + '\n')
    print('Letters you have tried that are not in the word:')
    print(wrong_guesses)
    print('\n')


def append_to_right_guess(letter, word):
    """
    Add correct guesses to right_guess list.

    :param letter: User guess
    :param word: Word chosen by computer to play game
    """
    for index, character in enumerate(word):
        if character == letter:
            location = index
            right_guesses[location] = letter


def is_letter_in_word(letter, word, player_name):
    """
    Indicates if user guess in the word chosen by computer.

    :param letter: User guess
    :param word: Word chosen by computer to play game
    :return: Boolean
    >>> is_letter_in_word('a', 'face', 'Jones')
    <BLANKLINE>
    Awesome job, Jones. The letter a is in the word
    <BLANKLINE>
    True
    >>> is_letter_in_word('a', 'house', 'Mary')
    <BLANKLINE>
    Sorry, Mary. The letter a is not in the word
    <BLANKLINE>
    False
    """

    if letter not in word:
        print('\nSorry, {}. The letter {} is not in the word\n'.format(player_name, letter))
        return False
    else:
        print('\nAwesome job, {}. The letter {} is in the word\n'.format(player_name, letter))
        return True


def player_guessed_word(right_guesses, word):
    """
    Checks if player guessed word.

    :param right_guesses: List containing user's right guesses
    :param word: Word chosen by computer to play game
    :return: Boolean
    >>> player_guessed_word([], 'house')
    False
    >>> player_guessed_word(['a'], 'house')
    False
    >>> player_guessed_word(['h', 'o', 'u', 's', 'e'], 'house')
    True
    """

    for letter in word:
        if letter not in right_guesses:
            return False
    return True

def calculate_player_score(player_name, remaining_guesses):
    """
    Gets player name and calculates score for current round
    :param player_name: a string
    :param current_score: integer
    :return: player score for current round and adds value to cumulative player score
    """
    #get user name
    #verify if user guessed word
    #if not return zero
    #if yes
        # give user 10 pts
        # get num of guesses remaining and multiply 10 by num of guesses remaining


def initialize_variables(current_word):
    """
    Initialize/reset variables based on current_word.
    :param current_word: Word chosen by computer to play game
    """
    global size, word, wrong_guesses, right_guesses, show_guesses
    word = current_word
    size = len(word)

    wrong_guesses = []
    right_guesses = [''] * size
    show_guesses = ''


def run_game():
    """
    Game loop
    """
    player_name = input('What is your name?\n')
    print('Hello {}! Try to guess the word I am thinking of.\n'.format(player_name))
    start_game = True
    while start_game:

        initialize_variables(get_local_word())
        print('The word you are trying to guess has {} letters.'.format(size))

        player_found_word = False
        guesses = 0
        while (len(wrong_guesses) < 6) and not player_found_word:
            remaining_guesses = 6 - guesses
            print('You have {} guesses remaining\n'.format(remaining_guesses))
            letter = input('Choose a letter: \n\n')
            if validate_input(letter):
                if is_letter_in_word(letter, word, player_name):
                    append_to_right_guess(letter, word)
                else:
                    wrong_guesses.append(letter)
                    guesses += 1
                if player_guessed_word(right_guesses, word):
                    player_found_word = True
                print_word(right_guesses, show_guesses)

        if player_found_word:
            print('Great job, {}! You guessed the word!'.format(player_name))
        else:
            print('You did not get it this time, {}. The word was: {}.'.format(player_name, word))

        new_round = input('Would you like to play again? Please enter yes or no (default: yes) > ')
        if new_round.lower() == 'no':
            start_game = False


if __name__ == "__main__":
    import doctest

    if doctest.testmod().failed == 0:
        run_game()
