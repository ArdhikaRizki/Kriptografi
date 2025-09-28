import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def vigenere_encrypt(plaintext: str, key: str) -> str:
    result = []
    key = key.lower()
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(key[j % len(key)]) - ord("a")
            if ch.isupper():
                result.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
            else:
                result.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
            j += 1
        else:
            # karakter non-alfabet dibiarkan tidak berubah
            result.append(ch)
    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    result = []
    key = key.lower()
    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(key[j % len(key)]) - ord("a")
            if ch.isupper():
                result.append(chr((ord(ch) - ord("A") - shift) % 26 + ord("A")))
            else:
                result.append(chr((ord(ch) - ord("a") - shift) % 26 + ord("a")))
            j += 1
        else:
            # karakter non-alfabet dibiarkan tidak berubah
            result.append(ch)
    return "".join(result)


def main_menu():
    while True:
        print("=== Vigenere Cipher ===")
        print("Pilih mode:")
        print("  e = Encrypt (Enkripsi)")
        print("  d = Decrypt (Dekripsi)")
        print("  q = Quit (Keluar)")
        mode = input("Input pilihan: ").strip().lower()
        clear_screen()

        if mode == "e":
            print("=== Vigenere Cipher ===\n")
            print("=== Encrypt ===")
            plaintext = input("Input Plaintext: ")
            key = input("Input Key (alfabet only, contoh: upnyk): ")
            if not key.isalpha(): # key harus alfabet
                print("Key tidak valid! Harus alfabet (A-Z).")
            else:
                hasil = vigenere_encrypt(plaintext, key)
                print("Hasil Enkripsi (Ciphertext):", hasil)

        elif mode == "d":
            print("=== Vigenere Cipher ===\n")
            print("=== Decrypt ===")
            ciphertext = input("Input Ciphertext: ")
            key = input("Input Key (alfabet only, contoh: upnyk): ")
            if not key.isalpha(): # key harus alfabet
                print("Key tidak valid! Harus alfabet (A-Z).")
            else:
                hasil = vigenere_decrypt(ciphertext, key)
                print("Hasil Dekripsi (Plaintext):", hasil)

        elif mode == "q":
            print("Program selesai")
            break

        else:
            print("Mode tidak valid! Pilih 'e', 'd', atau 'q'.")

        lagi = input("\nKembali ke menu? (y/n): ").strip().lower()
        if lagi != "y":
            print("Program selesai")
            break
        clear_screen()


if __name__ == "__main__":
    clear_screen()
    main_menu()
