def caesar_cipher(text, shift):
    result = []

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)

def main(message=None, choice=0):
    if message is None:
        message = input("Enter message: ")
    while choice not in [1, 2]:
        shift = int(input("Enter choice \n"
                            "1. Encrypt \n"
                            "2. Decrypt \n"))
        if choice == 1: # Encrypt
            shift = int(input("Enter shift (N)"))
            encrypted = caesar_cipher(message, shift)
            print("Encrypted message:", encrypted)
            
        elif choice == 2: # Decrypt
            shift = int(input("Enter shift (N)"))
            dencrypted = caesar_cipher(message, -shift)
            print("Decrypted message:", dencrypted)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()