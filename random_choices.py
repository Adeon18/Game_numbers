from random import choice 
def mixing_answers(num_1 :int, num_2 :int, num_3 :int, num_4 :int) -> tuple :
    '''
    Return the mixed string with possible answers and the correct answer. 
    Num_1 is always given as correct one.
    '''
    result = ''
    correct_letter = ''
    list = [num_1, num_2, num_3, num_4]
    first_choice = choice(list)
    result += 'A : ' + str(first_choice) #add the answer to string
    
    if first_choice == num_1 : #checking if A is correct
        correct_letter = 'A'
    list.remove(first_choice)

    second_choice = choice(list)
    result += ' B : ' + str(second_choice)

    if second_choice == num_1 :
        correct_letter = 'B'
    list.remove(second_choice)

    third_choice = choice(list)
    result += ' C : ' + str(third_choice)

    if third_choice == num_1 :
        correct_letter = 'C'
    list.remove(third_choice)

    fourth_choice = choice(list)
    result += ' D : ' + str(fourth_choice)

    if fourth_choice == num_1 :
        correct_letter = 'D'
    list.remove(fourth_choice)

    return (result, correct_letter)











     
