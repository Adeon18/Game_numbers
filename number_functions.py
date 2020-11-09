import random
from random import randint
from random_choices import mixing_answers

ULAM_NUMBERS = [26, 28, 36, 38, 47, 48, 53, 57, 62, 69, 72, 77, 82, 87, 97, 99, 102, 106, 114, 126, 131, 138, 145, 148]

def prime_number (number : int) -> bool :
    '''
    Return True if number is prime and False otherwise.
    >>> prime_number(73)
    True
    >>> prime_number(2) 
    True
    >>> prime_number(1)
    False
    >>> prime_number(24)
    False
    '''
    result = True
    if number == 1 :
        result = False
    for divisor in range(2, int(number**(1/2) + 1)) :
        if number % divisor == 0 :
            result = False
            break
    return result

def prime_numbers (m : int, n : int) -> list :
    '''
    Return the list of prime numbers between m and n.
    '''
    prime_list = []
    for number in range (m, n+1) :
        if prime_number(number) :
            prime_list.append(number)
    return prime_list



def ulam_number_initial (number : int) -> bool :
    '''
    Return True if number is Ulam's and False otherwise.
    >>> ulam_number(197)
    True
    >>> ulam_number(1)
    True
    >>> ulam_number(5)
    False
    >>> ulam_number(199)
    False
    '''
    result = False
    ulam_list = []
    ulam_list.append(1)
    ulam_list.append(2)
    for _ in range (3, number+1) :
        for potential_ulam_num in range (3, number+1) :
            count = 0
            for i in range (len(ulam_list)) :
                for j in range (i+1, len(ulam_list)) :
                    if ulam_list[i] + ulam_list[j] == potential_ulam_num and potential_ulam_num > max(ulam_list) :
                        count += 1
            if count == 1 :
                ulam_list.append(potential_ulam_num)
                break
    if number in ulam_list :
        result = True
    return result

def ulam_number (number : int) -> bool :
    return True if number in ULAM_NUMBERS else False

def next_ulam_number (number : int) -> int :
    '''
    Return the next Ulam number.
    >>> next_ulam_number(13)
    16
    >>> next_ulam_number(65)
    69
    >>> next_ulam_number(75)
    77
    >>> next_ulam_number(2)
    3
    '''
    new_bool = False
    i = 1
    while new_bool == False :
        if (number + i) in ULAM_NUMBERS:
            result = number + i
            new_bool = True
            #print('x')
        else :
            i+=1
            #print('y')
    return result

# for user :
def user_ulam_number () -> bool :
    '''
    Return True if user is right and False otherwise.
    '''
    result = False
    question = "Which number is the Ulam number?"
    number = randint(20, 150) #we random a number
    r_ulam_number = next_ulam_number(number) #we random an Ulam's number
    first_number = randint(r_ulam_number - 5, r_ulam_number - 1) #random other numbers
    second_number = randint (r_ulam_number - 20, r_ulam_number - 6)
    third_number = randint (r_ulam_number + 1, r_ulam_number + 10)
    if ulam_number(first_number) : #we don't want to have more than one Ulam's
        first_number+=1
    if ulam_number(second_number) : #there are no two consistent Ulam's numbers
        second_number+=1
    if ulam_number(third_number) :
        third_number+=1
    
    answers, correct_letter = mixing_answers(r_ulam_number, first_number, second_number, third_number)
    question += ' ' + answers

    return question, correct_letter.lower()

def user_next_ulam_number() -> bool :
    '''
    Return True if user is right and False otherwise.
    '''
    result = False
    number = randint(20, 150)
    question = "Which number is the next Ulam number after " +str(number) +' ?'
    r_ulam_number = next_ulam_number(number)
    first_number = randint(r_ulam_number - 5, r_ulam_number - 1)
    second_number = randint (r_ulam_number - 20, r_ulam_number - 6)
    third_number = randint (r_ulam_number + 1, r_ulam_number + 10)
    if ulam_number(first_number) :
        first_number+=1
    if ulam_number(second_number) :
        second_number+=1
    if ulam_number(third_number) :
        third_number+=1
    
    answers, correct_letter = mixing_answers(r_ulam_number, first_number, second_number, third_number)
    question += ' ' + answers
    print(question)
    #inputed_letter = input()
    #if inputed_letter == correct_letter :
    #    result = True
    return question, correct_letter.lower()




def lucky_number(number : int) -> bool :
    '''
    Return the list of lucky numbers till the meaning of n.
    >>> sieve_flavius(100)
    False
    >>> sieve_flavius(4)
    True
    >>> sieve_flavius(57)
    False
    '''
    result = False
    lucky_list = [i for i in range (1, number+1)] #creating a list
    deleting_number = 2
    idx = 1 #for next lucky number
    for _ in range(number-1) :
        if idx < len(lucky_list) :
            del lucky_list[deleting_number-1::deleting_number]
            deleting_number = lucky_list[idx]
            idx += 1
    if number in lucky_list :
        result = True
    return result

def next_lucky_number (number : int) -> int :
    '''
    Return the next lucky number
    '''
    new_bool = False
    i = 1
    while new_bool == False :
        if lucky_number(number+i) :
            result = number + i
            new_bool = True
        else :
            i+=1
    return result








def happy_number(number : int) -> bool :
    '''
    Return True if number is happy and False otherwise.
    >>> happy_number(12341000)
    True
    >>> happy_number(12345678)
    False
    >>> happy_number(66891)
    True
    '''
    result = False
    number = '{:08d}'.format(number)
    sum_1 = sum([int(num) for num in number[:4]])
    sum_2 = sum([int(num) for num in number[4:]])
    if sum_1 == sum_2:
        result = True
    return result

def happy_numbers(m : int,n : int) -> int :
    '''
    Return the list of happy numbers between m and n.
    >>> happy_numbers (6, 98)
    [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
    >>> happy_numbers (348576, 348596)
    [348584, 348593]
    '''
    happy_list = []
    for number in range (m, n+1) :
        if happy_number(number) :
            happy_list.append(number)
    return happy_list

def random_1_to_100():
    funcs = {'Ulam': ulam_number, 'happy': happy_number, 'prime': prime_number}
    randint = random.choice(range(100))
    rand_number_type = random.choice(list(funcs.keys()))
    question = 'Is {} a {} number?'.format(randint, rand_number_type)
    expected_key = 'y' if funcs[rand_number_type](randint) else 'n'
    return question, expected_key

def user_sieve_flavius () -> bool :
    '''
    '''
    result = False
    question = "Which number is lucky?"
    number = randint(20, 200)
    lucky_number = next_lucky_number(number)
    first_number = randint(lucky_number - 5, lucky_number - 1)
    second_number = randint (lucky_number - 20, lucky_number - 6)
    third_number = randint (lucky_number + 1, lucky_number + 10)
    answers, correct_letter = mixing_answers(lucky_number, first_number, second_number, third_number)
    question += ' ' + answers
    #print(question, correct_letter)
    #inputed_letter = input()
    #if inputed_letter == correct_letter :
        #result = True
    return question, correct_letter.lower()




def is_prime_number (number : int) -> bool :
    '''
    Return True if number is prime and False otherwise.
    >>> is_prime_number(73)
    True
    >>> is_prime_number(2)
    True
    >>> is_prime_number(1)
    False
    >>> is_prime_number(24)
    False
    '''
    result = True
    if number == 1 :
        result = False
    for divisor in range(2, int(number**(1/2) + 1)) :
        if number % divisor == 0 :
            result = False
            break
    return result


def random_number() -> int:
    """
    Returns a random number, which is not prime.
    """
    number = random.randrange(3, 1000)
    while is_prime_number(number):
        number = random.randrange(3, 1000)
    return number


def random_prime() -> int:
    """
    Returns a randomly generated prime number.
    """
    number = random.randrange(3, 1000)
    while not is_prime_number(number):
        number = random.randrange(3, 1000)
    return number


def two_numbers() -> list:
    """
    Returns a list of two random numbers, one is prime and other`s not.
    """
    two_nums = []
    n = random.randint(1, 100)
    while not is_prime_number(n):
        n = random.randint(1, 100)
    two_nums.append(n)
    while is_prime_number(n):
        n = random.randint(1, 100)
    two_nums.append(n)
    return two_nums


def two_primes() -> list:
    """
    Returns a list of two primes.
    """
    two_primes_list = []
    for _ in range(2):
        n = random.randint(1, 100)
        while not is_prime_number(n):
            n = random.randint(1, 100)
        two_primes_list.append(n)
    return two_primes_list


def next_prime(n: int) -> int:
    """
    Returns the next prime after the taken one.
    """
    next_bool = False
    i = 1
    while not next_bool:
        if is_prime_number(n + i):
            result = n + i
            break
        i += 1
    return result


def random_prime_in_range(m: int, n: int) -> int:
    """
    Returns a random prime from between m and n.
    """
    number = random.randint(m, n)
    while not is_prime_number(number):
        number = random.randint(m, n)
    return number


def is_prime_usercheck() -> bool:
    """
    Returns multiple choices for 'is prime' question and a correct letter.
    """
    question = "Which number is prime?"
    prime_number = random_prime()
    first_number = random_prime() - 1
    second_number = random_prime() - 1
    third_number = random_prime() - 1
    answers, correct_letter = mixing_answers(prime_number,
        first_number, second_number, third_number)
    question += " " + answers

    return question, correct_letter.lower()

def prime_pair_usercheck() -> bool:
    """
    Returns multiple choices for 'prime pair' question and a correct letter.
    """
    question = "Both numbers are prime:"
    prime_pair = two_primes()
    first_pair = two_numbers()
    second_pair = two_numbers()
    third_pair = two_numbers()
    answers, correct_letter = mixing_answers(prime_pair, first_pair,
        second_pair, third_pair)

    question += " " + answers

    return question, correct_letter.lower()


def next_prime_usercheck() -> bool:
    """
    Returns a multiple coice for the next prime questions and a correct letter.
    """
    number = random_prime_in_range(200, 500)
    question = "What is the next prime number after {a}?".format(a = number)
    first_number =  random.randint(200, 500)
    second_number = random.randint(200, 500)
    third_number = random.randint(200, 500)
    fourth_number = next_prime(number)
    answers, correct_letter = mixing_answers(first_number, second_number, third_number, fourth_number)

    question += " " + answers

    return question, correct_letter.lower()




def theQuestion():
    funcs = [(random_1_to_100, True), (user_ulam_number, False), (user_sieve_flavius, False), (user_next_ulam_number, False), (is_prime_usercheck, False), (next_prime_usercheck, False), (prime_pair_usercheck, False)]
    func, yesno = random.choice(funcs)
    return func(), yesno

    



if __name__ == '__main__':
    print(theQuestion())
