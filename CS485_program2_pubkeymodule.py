# Michael Long
# CS485
# Program #2: Public Key Cryptography
# Encrypt / Decrypt Module

from random import getrandbits, seed, randrange

def encrypt(m, p, g, e2):

    try:
        k = randrange(0, p-1)
        c1 = pow(g, k, p)
        c2_temp = pow(e2, k, p)
        c2_temp_m = m % p
        c2 = (c2_temp * c2_temp_m) % p
        return c1, c2

    except Exception:
        print("Error, encryption failed")
        return -1

def decrypt(c1, c2, p, g, d):

    try:
        c1_temp = pow(c1, p-1-d, p)
        c2_temp = c2 % p
        m = (c1_temp * c2_temp) % p
        return m

    except Exception:
        print("Error, decryption failed")
        return -1

def key_gen(arg):

    try:
        seed(arg)
        p = _generate_random_prime(32)
        g = 2
        d = randrange(0, p)
        e2 = pow(g, d, p)
        print(f'Public Key Info: {p} {g} {e2}')
        print(f'Private Key Info: {p} {g} {d}')
        # Public Key Info
        f = open('pubkey.txt', mode = 'w')
        f.write(f'{p} {g} {e2}')
        f.close()
        # Private Key Info
        f = open('prikey.txt', mode = 'w')
        f.write(f'{p} {g} {d}')
        f.close

    except Exception:
        print("Error, key generation failed")
        return -1

    return 0

def _generate_random_prime(arg):

    prime_flag = False
    while (prime_flag == False):

        # Generate the q value
        q = _random_odd(arg)
        #print(q)
        prime_flag = _miller_rabin(q, 100)
        if (prime_flag == True):
            if ((q % 12) == 5):
                # Prime has been found, test p
                p = ((2 * q) + 1)
                if (p > 2**(arg)):
                    print("Error, too big")
                prime_flag = _miller_rabin(p, 100)
            else:
                prime_flag = False
        
    return p

def _random_odd(arg):

    ret = getrandbits(arg-1)   # Generate random number of length 'arg' - 1 bits
    ret = ret | (1 << (arg-2)) # Make sure that the second left most bit is 1
    ret = ret | 1              # Make sure that the rightmost bit is 1 to have an odd number
    return ret



def _miller_rabin(arg, precision):

    # Check base case (arg shouldn't be even or less than 3)
    if (arg & 1 == 0 or arg < 3): 
        return -1

    m = arg - 1
    k = 0

    # Put arg in terms of k and m (or arg - 1 = 2^k * m)
    while (m & 1 != 0):
        m = m >> 1
        k += 1
        

    a = randrange(2, arg - 2)
    x = pow(a, m, arg)

    if (x % arg == 1 or x % arg == arg-1):
        return True

    for i in range(k):
        x = pow(x, 2, arg)
        if (x == 1):
            return False
        if (x == arg-1):
            return True

    return False