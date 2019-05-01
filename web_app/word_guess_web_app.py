import random
import requests
import os

word = ''
size = len(word)

wrong_guesses = []
right_guesses = [''] * size
show_guesses = ''
leaderboard_file = 'leaderboard'


class LetterRound:
    def __init__(self, word):
        self.word = word #attribute

    def validate_input(self, letter):
        """
        Verifies validity of user input.

        :param letter: User guess
        :return: Boolean
        >>> letter_round = LetterRound('casa')
        >>> letter_round.validate_input('abc')
        Please enter a single letter
        <BLANKLINE>
        False
        >>> letter_round.validate_input('abc123')
        Please enter a letter
        <BLANKLINE>
        False
        >>> letter_round.validate_input('a')
        True
        >>> letter_round.validate_input('3')
        Please enter a letter
        <BLANKLINE>
        False
        >>> letter_round.validate_input('')
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

    def player_guessed_word(self, right_guesses):
        """
        Checks if player guessed word.

        :param right_guesses: List containing user's right guesses
        :param word: Word chosen by computer to play game
        :return: Boolean
        >>> letter_round = LetterRound('house')
        >>> letter_round.player_guessed_word([])
        False
        >>> letter_round.player_guessed_word(['a'])
        False
        >>> letter_round.player_guessed_word(['h', 'o', 'u', 's', 'e'])
        True
        """

        for letter in self.word:
            if letter not in right_guesses:
                return False
        return True

    def append_to_right_guess(self, letter):
        """
        Add correct guesses to right_guess list.

        :param letter: User guess
        :param word: Word chosen by computer to play game
        """
        for index, character in enumerate(self.word):
            if character == letter:
                location = index
                right_guesses[location] = letter

    def is_letter_in_word(self, letter, player_name):
        """
        Indicates if user guess in the word chosen by computer.

        :param letter: User guess
        :param word: Word chosen by computer to play game
        :return: Boolean
        >>> letter_round = LetterRound('face')
        >>> letter_round.is_letter_in_word('a', 'Jones')
        <BLANKLINE>
        Awesome job, Jones. The letter a is in the word
        <BLANKLINE>
        True
        >>> letter_round.is_letter_in_word('z', 'Mary')
        <BLANKLINE>
        Sorry, Mary. The letter z is not in the word
        <BLANKLINE>
        False
        """

        if letter not in self.word:
            print('\nSorry, {}. The letter {} is not in the word\n'.format(player_name, letter))
            return False
        else:
            print('\nAwesome job, {}. The letter {} is in the word\n'.format(player_name, letter))
            return True


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


def get_local_word():
    """
    Local function for offline use.
    """
    words = ['house', 'casa']
    word = random.choice(words)
    return word


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



def calculate_player_score(remaining_guesses):
    """
    Calculates score for current round
    :param remaining_guesses: integer
    :return: player score for current round
    >>> calculate_player_score(2)
    20
    >>> calculate_player_score(0)
    0
    >>> calculate_player_score(4)
    40
    """
    score = 10 * remaining_guesses
    return score


def add_to_leaderboard(player, score):
    """
    Adds score for current round to player name in leaderboard
    :param player: a string
    :param score: player score for current round
    :return: total player score
    """
    # file looks like this:
    # joe=40
    # bob=50
    leaderboard = ''
    leaderboard_score = 0
    player_not_in_leaderboard = True
    if os.path.isfile(leaderboard_file):
        with open(leaderboard_file, 'r') as file:
            for line in file:
                if line.startswith(player + '='):
                    words = line.split('=')
                    leaderboard_score = score + int(words[1])
                    leaderboard += player + '=' + str(leaderboard_score) + '\n'
                    player_not_in_leaderboard = False
                else:
                    leaderboard += line

    if player_not_in_leaderboard:
        leaderboard_score = score
        leaderboard += player + '=' + str(leaderboard_score) + '\n'

    with open(leaderboard_file, 'w+') as file:
        file.write(leaderboard)

    return leaderboard_score


def show_top_five_on_leaderboard():
    """
    Prints the top 5 scores on leaderbaoard.
    """
    all_scores = []
    with open(leaderboard_file, 'r') as file:
        for line in file:
            words = line.split('=')
            leaderboard_score = int(words[1])
            player = words[0]
            all_scores.append((leaderboard_score, player))
    print('Here are the current top 5 players in the leaderboard:')
    sorted_scores = sorted(all_scores, reverse=True)[0:5]
    for score, name in sorted_scores:
        print('{} - {}'.format(name, score))


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
    # player_name = input('What is your name?\n')
    # print('Hello {}! Try to guess the word I am thinking of.\n'.format(player_name))
    # start_game = True
    # while start_game:

        # initialize_variables(get_word_from_api())
        # print('The word you are trying to guess has {} letters.'.format(size))
        #
        # player_found_word = False
        # guesses = 0
        # while (len(wrong_guesses) < 6) and not player_found_word:
        #     remaining_guesses = 6 - guesses
        #     print('You have {} guesses remaining\n'.format(remaining_guesses))
            #letter_round = LetterRound(word)
            #letter = input('Choose a letter: \n\n')
    if letter_round.validate_input(letter):
        if letter_round.is_letter_in_word(letter, player_name):
            letter_round.append_to_right_guess(letter)
        else:
            wrong_guesses.append(letter)
            guesses += 1
        if letter_round.player_guessed_word(right_guesses):
            player_found_word = True
        print_word(right_guesses, show_guesses)

    if player_found_word:
        print('Great job, {}! You guessed the word!'.format(player_name))
        player_score = calculate_player_score(remaining_guesses)
        print('You scored {} points in this round.\n'.format(player_score))
        total_score = add_to_leaderboard(player_name, player_score)
        show_top_five_on_leaderboard()
        print('\nHere is your score in the leaderboard: {}'.format(total_score))
    else:
        print('You did not get it this time, {}. The word was: {}.'.format(player_name, word))

    new_round = input('Would you like to play again? Please enter yes or no (default: yes) > ')
    if new_round.lower() == 'no':
        start_game = False


if __name__ == "__main__":
    import doctest

    if doctest.testmod().failed == 0:
        run_game()
