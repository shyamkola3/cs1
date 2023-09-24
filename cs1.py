import sys
import string

def check_key(key, keylength):
    if len(key) != keylength:
        print("Error: <keylength> does not match the length of <key>")
        sys.exit(1)
    if sorted(key) != [str(i) for i in range(1, keylength + 1)]:
        print("Error: <key> must include all digits from 1 to <keylength> with each digit occurring exactly once.")
        sys.exit(1)

def check_inputfile(inputfile):
    with open(inputfile, 'r') as file:
        data = file.read()
        if not data.isalnum():
            print("Error: <inputfile> must contain only lowercase letters (a-z) or digits (0-9).")
            sys.exit(1)

def encrypt(key, inputfile, outputfile):
    with open(inputfile, 'r') as file:
        data = file.read().replace("\n", "")

    key = list(key)
    key_order = sorted(range(len(key)), key=lambda k: key[k])

    padding = (len(key) - len(data) % len(key)) % len(key)
    data += 'z' * padding

    encrypted = [''] * len(key)
    for i, char in enumerate(data):
        encrypted[key_order[i % len(key)]] += char

    with open(outputfile, 'w') as file:
        file.write(''.join(encrypted))

def decrypt(key, inputfile, outputfile):
    with open(inputfile, 'r') as file:
        data = file.read().replace("\n", "")

    key = list(key)
    key_order = sorted(range(len(key)), key=lambda k: key[k])

    chunk_size = len(data) // len(key)
    remainder = len(data) % len(key)

    decrypted = [''] * len(data)
    index = 0

    for k in key_order:
        length = chunk_size + (1 if k < remainder else 0)
        decrypted[index:index + length] = data[k::len(key)]
        index += length

    with open(outputfile, 'w') as file:
        file.write(''.join(decrypted))

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: python row_transposition.py <keylength> <key> <inputfile> <outputfile> <enc/dec>")
        sys.exit(1)

    keylength = int(sys.argv[1])
    key = sys.argv[2]
    inputfile = sys.argv[3]
    outputfile = sys.argv[4]
    mode = sys.argv[5]

    check_key(key, keylength)
    check_inputfile(inputfile)

    if mode == 'enc':
        encrypt(key, inputfile, outputfile)
        print(f"File '{inputfile}' encrypted successfully to '{outputfile}'")
    elif mode == 'dec':
        decrypt(key, inputfile, outputfile)
        print(f"File '{inputfile}' decrypted successfully to '{outputfile}'")
    else:
        print("Error: <enc/dec> must be either 'enc' for encryption or 'dec' for decryption.")
        sys.exit(1)
