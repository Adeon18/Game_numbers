''' Back-end for the labyrinth game '''

import settings import *

class Gameplay():
    ''' All the gameplay scenario happens here '''
    
    def __init__(self, mode = 'std'):
        ''' Initializes the game '''

        self.current_difficulty = 1
        self.eggs_found = 0
        self.eggs_total = 5
        self.xp = 10
        self.keys = 0
        self.current_boss_xp = BOSS_XP
        self.current_egg_xp = EGG_XP
        self.mode = mode


    def changexp(self, delta):
        ''' Changes player's xp by a given delta '''

        self.xp += delta
        if self.xp <= 0:
            self.event_handler('lost')

    def std_question_scenario(self):
        ''' The most common question-answer scenario '''
        
        if self.question():
            self.changexp(1)
        else:
            self.changexp(-1)


    def question(self, diff_level = 'std'):
        ''' Asks player a question of a given difficulty '''
        
        if diff_level == 'std':
            diff_level = self.current_difficulty
        # ask a question of a given difficulty
        print('[question asked]')
        result = bool(input('Your answer:'))
        print('Correct! XP increased' if result else 'Wrong! XP decreased')
        return result

    def event_handler(self, event):
        ''' A handler for all events in the game. '''

        if event == 'egg encountered':
            print('new egg found;')
            if self.keys >= self.current_egg_xp:
                self.std_question_scenario()
            else:
                print('[unable to ask a question; not enough keys!]')
            
        if event == 'key found':
            self.keys += 1
            print('new key found; total keys:', self.keys)
            return 'key found'

        if event == 'boss encountered':
            print('boss encountered; starting a question sequence...')
            for i in range(3):
                if not self.question():
                    self.changexp(-5)
                    return self.event_handler('lost against boss')
            return self.event_handler('won against boss')

        if event == 'won against boss':
            self.changexp(100)
            print('CONGRATULATIONS! YOUR POINTS:', self.xp)
            return 'quit'

        if event == 'lost against boss':
            self.changexp(-100)
            print('GAME OVER; POINTS:', self.xp)
            return 'quit'

        print('Total XP:', self.xp)
        return None


if __name__ == '__main__':
    ''' Initiates the classic gameplay scenario '''
    gameplay = Gameplay()
    while True:
        # emitting the gameplay in console
        event = input('Event: ')
        handling_result = gameplay.event_handler(event)
        print(handling_result)
        if handling_result == 'quit':
            print('[infinite loop ended]')
            break
