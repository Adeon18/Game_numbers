
import random

from main import Program
from number_functions import *


def question(diff_level='std'):
    ''' Asks player a question of a given difficulty '''

    if diff_level == 'std':
        #diff_level = self.current_difficulty
        question, expected_answer = '[question goes here]', 'yes'
    # ask a question of a given difficulty

    elif diff_level == 'rand':
        funcs = {'Ulam': ulam_number, 'happy': happy_number, 'prime': prime_number}
        randint = random.choice(range(100))
        rand_number_type = random.choice(list(funcs.keys()))
        print('Question: is', randint, 'a', rand_number_type, 'number?')
        expected_answer = 'yes' if funcs[rand_number_type](randint) else 'no'
        print('Expected answer:', expected_answer)
    else:
        return None

    Program.wait_for_key(Program)

    #if result == expected_answer:
    print('Correct! XP increased')
    return True
    # print('Wrong! XP decreased')
    # return False