def firstNPrimes(n):
    '''
    Returns an array containing the first 'n' prime numbers along the number line.

    Args:
        n (int): The number of prime numbers to generate.

    Returns:
        list: A list of the first 'n' prime numbers.
        None: If 'n' is equal to 0.
    '''
    if n==0:
        return None
    if n<0:
        return "<'n' must be positive integer>"
    primes = [2]
    num = 3
    while len(primes) < n:
        isPrime = True
        for j in range(len(primes)):
            if primes[j]**2 > num:
                break
            if  num%primes[j]==0:
                isPrime = False
                break
        if isPrime:
            primes.append(num)
        num += 2
    return primes