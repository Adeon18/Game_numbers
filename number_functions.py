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









def ulam_number (number : int) -> bool :
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

def ulam_numbers (m : int, n : int) -> int :
    '''
    Return the list of ulam numbers between m and n.
    >>> ulam_numbers(100, 200)
    [102, 106, 114, 126, 131, 138, 145, 148, 155, 175, 177, 180, 182, 189, 197]
    >>> ulam_numbers(1, 20)
    [1, 2, 3, 4, 6, 8, 11, 13, 16, 18]
    >>> ulam_numbers(30, 50)
    [36, 38, 47, 48]
    >>> ulam_numbers(60, 90)
    [62, 69, 72, 77, 82, 87]
    '''
    ulam_list = []
    for number in range (m, n+1) :
        if ulam_number(number) :
            ulam_list.append(number)
    return ulam_list














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



if __name__ == '__main__':
    print(happy_number(10000001))
