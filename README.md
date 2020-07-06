Foreword: This is a demonstration of implementing an encryption algorithm and has not been vetted by the Cryptographic Community at large, this has been made for learning purposes, and not to be used in any application.

1) Michael Long, michael.long.code@gmail.com
2) CS485 Public / Private key implementation using 32 bit keys and messages. Key length can be variable
3) Program is run with "python3 CS485_program2_main.py"
4) List of files:
  - "CS485_program2_main.py" -- executes the test body to verify functionality of code
  - "CS485_program2_pubkeymodule.py" -- houses the functions to do key generation, prime generation, Miller-Rabin, encryption, and decryption
  - "pubkey.txt" -- Contains the output public key elements of "key_gen" with values: "p", "g", and "e2" defined in Project specification
  - "prikey.txt" -- Contains the output private key elements of "key_gen" with values: "p", "g", and "d" defined in Project specification
  - "ptext.txt" -- A sample plain text, will be deleted and recreated through the test code to verify functionality of encryption
  - "ctext.txt" -- Generated cipher text pairs "c1" and "c2" from encryption of data in "ptext.txt", used to verify functionality of decryption
