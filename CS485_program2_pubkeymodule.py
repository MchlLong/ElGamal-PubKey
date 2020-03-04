# Michael Long
# CS485
# Program #2: Public Key Cryptography
# Encrypt / Decrypt Module

from random import getrandbits, seed, randrange

def encrypt(m, p, g, e2):
    """
    Function which takes some plain text input 'm', and generates cipher text 'c1' and 'c2'
    - 'c1' is generated by calculating 'g^k mod p' where 'g' is a generator value, 'k' is some random value less than or equal to large 
    public prime 'p', and 'p' is a large public prime
    - 'c2' is generated by calculating 'e2^k * m mod p' where 'e2' is the generator to the power of the secret key, 'k 'is some random value 
    less than or equal to large prime 'p', and 'p' is a large public prime
    """
    try:
        k = randrange(0, p-1)           # Pick some random value to encrypt with per encryption
        c1 = pow(g, k, p)               # Calculate g^k mod p using "Square and Multiply" built into "pow" function
        c2_temp = pow(e2, k, p)         # Calculate e2^k mod p using "Square and Multiply" built into "pow" function
        c2_temp_m = m % p               # Calculate m mod p
        c2 = (c2_temp * c2_temp_m) % p  # Apply modulo math principle a*b mod p = ((a mod p) (b mod p)) mod p
        return c1, c2                   # Return cipher text pair

    except Exception:
        print("Error, encryption failed")
        return -1

def decrypt(c1, c2, p, g, d):
    """
    Function which takes some cipher text input 'c1', and 'c2', and generates plain text 'm'
    - 'm' is generated by calculating ((c1^(p-1-d) mod p)*(c2 mod p)) mod p where 'c1' and 'c2' are a pair of cipher text values, 'p' is a large
    public prime, 'g' is a generator value, and 'd' is a the private key value.
    """
    try:
        c1_temp = pow(c1, p-1-d, p) # Compute c1^(p-1-d) mod p using "Square and Multiply" built into "pow" function
        c2_temp = c2 % p            # Compute c2 mod p
        m = (c1_temp * c2_temp) % p # Apply modulo math principle a*b mod p = ((a mod p) (b mod p)) mod p
        return m                    # Return original message

    except Exception:
        print("Error, decryption failed")
        return -1

def key_gen(arg):

    try:
        seed(arg)                               # Randomize values based on a seed
        p = _generate_random_prime(32)          # Generate a prime of length 32 bits
        g = 2                                   # Generator value of 2
        d = randrange(0, p)                     # Pick a random secret key value
        e2 = pow(g, d, p)                       # Compute 'e2' to post in public key
        print(f'Public Key Info: {p} {g} {e2}') # Print Public Key info for verification
        print(f'Private Key Info: {p} {g} {d}') # Print Private Key info for verification
        # Public Key Info
        f = open('pubkey.txt', mode = 'w')      # Write public key to a file
        f.write(f'{p} {g} {e2}')
        f.close()
        # Private Key Info
        f = open('prikey.txt', mode = 'w')      # Write private key to a file
        f.write(f'{p} {g} {d}')
        f.close

    except Exception:
        print("Error, key generation failed")
        return -1

    return 0

def _generate_random_prime(arg):
    """
    Function to generate a random prime value 'p' from a seed value 'arg' to be used for public key encryption, 
    validated with Miller-Rabin and tested to make sure that the prime can be generated with a 'g' value of 2.
    - 
    """
    prime_flag = False           # Prime flag used to keep checking until a prime has been found and passes Miller-Rabin tests
    while (prime_flag == False):

        q = _random_odd(arg)                  # Generate 'q 'to base large prime 'p' on
        prime_flag = _miller_rabin(q)         # Validate that 'q' is prime
        if (prime_flag == True):              # If 'q' is prime, then test to make sure a generator, 'g', of 2 will work
            if ((q % 12) == 5):               # Test to make sure a generator, 'g', of 2 will work
                p = ((2 * q) + 1)             # Pick prime 'p' 
                prime_flag = _miller_rabin(p) # Test to make sure 'p' is still prime and that 'g' and 'q' are coprimes
            else:
                prime_flag = False            # If fails, go back into loop and repeat
        
    return p

def _random_odd(arg):
    """
    Function to generate a bit string of length 'arg', sets the high bit and low bit to 1 to guarantee a number of
    bits equal to the length 'arg'
    """
    ret = getrandbits(arg-1)   # Generate random number of length 'arg' - 1 bits
    ret = ret | (1 << (arg-2)) # Make sure that the second left most bit is 1
    ret = ret | 1              # Make sure that the rightmost bit is 1 to have an odd number
    return ret



def _miller_rabin(arg):
    """
    Function to check whether or not 'arg' is a prime number, uses Miller-Rabin Primality test to determine whether
    or not the value 'arg' is prime. 
    """
    # Check base case (arg shouldn't be even or less than 3)
    if (arg & 1 == 0 or arg < 3): 
        return -1

    m = arg - 1 # Remove 1 to figure out which value will fit arg - 1
    k = 0       # 'k' is last valid exponent that produces no remainder

    # Put arg in terms of k and m (or arg - 1 = 2^k * m)
    while (m & 1 != 0): # Check that the number is dividing evenly with no remainder
        m = m >> 1      # Divide 'm' value by 2
        k += 1          # Increment the power 'k'
        

    a = randrange(2, arg - 2) # Pick a random value 'a' to test Miller-Rabin with
    x = pow(a, m, arg)        # Compute a^m mod p using "Square and Multiply" built into "pow" function

    if (x % arg == 1 or x % arg == arg-1): # If 'x' is 1 or congruent to -1 mod arg (which is arg - 1) then the value is prime
        return True

    for i in range(k):     # Loop through previously calculated range of potential values in k
        x = pow(x, 2, arg) # Compute x^2 mod p using "Square and Multiply" built into "pow" function
        if (x == 1):       # If 'x' is 1, value is not prime
            return False 
        if (x == arg-1):   # If 'x' is congruent to -1 mod arg (which is arg - 1) then the value is prime
            return True

    return False           # If code reaches this point after checking k loops, then the value is assumed composite