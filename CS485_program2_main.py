# Michael Long
# CS485
# Program #2: Public Key Cryptography
# Main


import CS485_program2_pubkeymodule as pubkey
import re as regex
def main():
    
    print('Initialization Pretesting')
    print('Testing Miller Rabin on a large prime')
    print(pubkey._miller_rabin(219345360441335241530872580507741777443))
    print('Testing Random Prime Generation p and q')
    print(pubkey._generate_random_prime(32))
    
    # Demo Key Generation, Encryption, and Decryption

    # Key Generation
    print('Running demo')
    print('Generating keys, writing to \'pubkey.txt\' and \'prikey.txt\'')
    pubkey.key_gen(12345)
    
    # Encryption
    print('Beginning Encryption')
    print('Reading in \'ptext.txt\' and \'pubkey.txt\'')
    f = open('ptext.txt', mode = 'r')
    message = f.read()
    f.close
    f = open('ctext.txt', mode = 'w').close()

    print(f'Plain Text: {message}')
    print(f'Generating Keys')
    
    f = open('pubkey.txt', mode = 'r')
    public_key = f.readline()
    f.close   
    public_key = public_key.split()
    p = int(public_key[0])
    g = int(public_key[1])
    e2 = int(public_key[2])

    print("Converting Plain Text into messages")
    message = list(message)
    len_msg, len_pad = divmod(len(message), 4)

    for i in range(len_msg):
        print(f'Encrypting m block #: {i}')
        temp_msg = [0,0,0,0]
        for j in range(4):
            temp_msg[j] = ord(message[i*4 + j]) 
            temp_msg[j] = temp_msg[j] << (8 * (3-j))
        to_encrypt = temp_msg[0] | temp_msg[1] | temp_msg[2] | temp_msg[3]

        print(f'Plaintext: {to_encrypt}')
        c = pubkey.encrypt(to_encrypt, p, g, e2)
        print(f'Cipher Text: {c}')

        f = open('ctext.txt', mode = 'a')
        f.write(f'{c[0]} {c[1]}\n')
        f.close()

    # Encrypt residual message stuff
    if (len_pad != 0):
        print(f'Encrypting residual message')
        temp_msg = [0,0,0,0]
            
        for i in range(len_pad):
            temp_msg[i] = ord(message[len_msg*4 + i]) 
            temp_msg[i] = temp_msg[i] << (8 * (3-i))
        to_encrypt = temp_msg[0] | temp_msg[1] | temp_msg[2] | temp_msg[3]

        print(f'Plaintext: {to_encrypt}')
        c = pubkey.encrypt(to_encrypt, p, g, e2)
        print(f'Cipher Text: {c}')

        f = open('ctext.txt', mode = 'a')
        f.write(f'{c[0]} {c[1]}\n')
        f.close()

    # Decryption
    print('Beginning Decryption')
    print('Reading in \'ctext.txt\' and \'prikey.txt\'')

    # Get Private Key to decrypt with
    f = open('prikey.txt', mode = 'r')
    private_key = f.readline()
    f.close
    private_key = private_key.split()
    p = int(private_key[0])
    g = int(private_key[1])
    d = int(private_key[2])

    # Open cipher text and begin decryption
    f = open('ctext.txt', mode = 'r')
    message = f.read()
    f.close()
    message = message.split()

    # Empty plaintext to demonstrate decryption
    f = open('ptext.txt', mode = 'w').close()

    for i in range(len(message) // 2):
        to_write = [0, 0, 0, 0]
        temp_msg = pubkey.decrypt(int(message[i*2 + 0]), int(message[i * 2 + 1]), p, g, d)
        for j in range(4):
            to_write[j] = int((temp_msg >> (3-j) * 8) & 0xFF)
            to_write[j] = chr(to_write[j])
            if (to_write[j] != chr(0)):
                f = open('ptext.txt', mode = 'a', newline='')
                f.write(to_write[j])
                f.close()

    print("Finished demo")
    

if __name__ == '__main__':
    main()