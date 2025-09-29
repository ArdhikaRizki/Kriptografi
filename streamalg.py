import itertools

#Keystream Generator (LFSR) 
def lfsr(seed, taps, length):
    sr = seed[:]
    for _ in range(length):
        out = sr[-1]
        yield out
        feedback = 0
        for t in taps:
            feedback ^= sr[t]
        sr = [feedback] + sr[:-1]

#XOR helper
def xor_bits(data_bits, key_bits):
    return [d ^ k for d, k in zip(data_bits, key_bits)]

#string <-> bits converter
def str_to_bits(text):
    return list(itertools.chain.from_iterable(
        [(ord(c) >> i) & 1 for i in range(7, -1, -1)] for c in text
    ))

def bits_to_str(bits):
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b+8]
        if len(byte) < 8:
            break
        val = 0
        for bit in byte:
            val = (val << 1) | bit
        chars.append(chr(val))
    return ''.join(chars)

#Stream Cipher
def stream_encrypt(plaintext, seed, taps):
    bits = str_to_bits(plaintext)
    keystream = list(lfsr(seed, taps, len(bits)))
    cipher_bits = xor_bits(bits, keystream)
    return ''.join(str(b) for b in cipher_bits)

def stream_decrypt(cipher_str, seed, taps):
    cipher_bits = [int(b) for b in cipher_str]   # turn "1011" back into [1,0,1,1]
    keystream = list(lfsr(seed, taps, len(cipher_bits)))
    plain_bits = xor_bits(cipher_bits, keystream)
    return bits_to_str(plain_bits)

#UI
def streammenu():
    while True:
        print("\n=== Stream Cipher Menu ===")
        print("1. Encrypt Text")
        print("2. Decrypt Cipher")
        print("3. Exit")

        choice = input("Choose (1-3): ")

        if choice == "1":
            text = input("Enter plaintext: ")
            seed_str = input("Enter seed bits (e.g. 1001): ")
            seed = [int(b) for b in seed_str]
            taps = [0, len(seed)-1]  # contoh taps: bit pertama & terakhir
            cipher = stream_encrypt(text, seed, taps)
            print("Cipher (bits):", ''.join(str(b) for b in cipher))

        elif choice == "2":
            cipher_str = input("Enter cipher bits (string of 0/1): ")
            cipher = [int(b) for b in cipher_str]
            seed_str = input("Enter seed bits (e.g. 1001): ")
            seed = [int(b) for b in seed_str]
            taps = [0, len(seed)-1]
            plain = stream_decrypt(cipher, seed, taps)
            print("Decrypted text:", plain)

        elif choice == "3":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

