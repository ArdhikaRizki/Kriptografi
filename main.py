# print("Hello, World!")
# print("this is for a all in one file test")
from typing import List
from caesarchipher import caesar_cipher 
from des_algorithm import des_encrypt_ecb, des_decrypt_ecb
from vigenere_algorithm import vigenere_encrypt, vigenere_decrypt
from streamalg import stream_decrypt, stream_encrypt 
# from utils import clear_screen, str_to_bytes, bytes_to_str
import streamlit as st


# =========================
# STREAMLIT UI
# =========================
import streamlit as st
import base64

# ==================================
# Asumsinya function kamu sudah ada:
# caesar_cipher(text, shift)
# vigenere_encrypt(plaintext, key)
# vigenere_decrypt(ciphertext, key)
# stream_encrypt(plaintext, seed, taps)
# stream_decrypt(cipher_bits, seed, taps)
# des_encrypt_ecb(plaintext: bytes, key: bytes) -> bytes
# des_decrypt_ecb(ciphertext: bytes, key: bytes) -> bytes
# ==================================

st.set_page_config(page_title="Crypto Playground", page_icon="🔐", layout="wide")
st.title("🔐 Crypto Playground")

# Pilih algoritma
algo = st.sidebar.selectbox(
    "Pilih Algoritma",
    ["Caesar Cipher", "Vigenere Cipher", "Stream Cipher", "DES", "Enkripsi Super"]
)

# Pilih mode
mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True)

# Input sesuai algoritma
if algo == "Caesar Cipher":
    text = st.text_area("Masukkan Teks")
    shift = st.number_input("Shift (integer)", value=3)
    if st.button("Proses"):
        result = caesar_cipher(text, shift if mode=="Enkripsi" else -shift)
        st.success("Hasil:")
        st.code(result)

elif algo == "Vigenere Cipher":
    text = st.text_area("Masukkan Teks")
    key = st.text_input("Key (string)")
    if st.button("Proses"):
        if mode == "Enkripsi":
            result = vigenere_encrypt(text, key)
        else:
            result = vigenere_decrypt(text, key)
        st.success("Hasil:")
        st.code(result)

elif algo == "Stream Cipher":
    text = st.text_area("Masukkan Teks")
    seed_int = st.number_input("Seed (integer)", value=9)

   
    def int_to_bits(n, width=8):
        return [(n >> i) & 1 for i in range(width-1, -1, -1)]

    seed = int_to_bits(int(seed_int), width=8)

   
    taps = [0, len(seed)-1]

    if st.button("Proses"):
        if mode == "Enkripsi":
            result = stream_encrypt(text, seed, taps)
        else:
            cipher_bits = [int(b) for b in text.strip()]
            result = stream_decrypt(cipher_bits, seed, taps)
        st.success("Hasil:")
        st.code(result)


elif algo == "DES":
    text = st.text_area("Masukkan Plaintext (untuk Enkripsi) atau Cipher (base64 untuk Dekripsi)")
    key = st.text_input("Key (8 karakter)")
    if st.button("Proses"):
        if len(key) != 8:
            st.error("Key harus 8 karakter!")
        else:
            if mode == "Enkripsi":
                cipher_bytes = des_encrypt_ecb(text.encode(), key.encode())
                result = base64.b64encode(cipher_bytes).decode()
            else:
                try:
                    cipher_bytes = base64.b64decode(text.encode())
                    plain_bytes = des_decrypt_ecb(cipher_bytes, key.encode())
                    result = plain_bytes.decode()
                except Exception as e:
                    st.error(f"Error: {e}")
                    result = None
            if result:
                st.success("Hasil:")
                st.code(result)
                
elif algo == "Enkripsi Super":
    text = st.text_area("Masukkan Plaintext (untuk Enkripsi) atau Cipher (base64 untuk Dekripsi)")

    # Fixed sequence: Caesar -> Vigenere -> Stream -> DES
    st.write("### Konfigurasi Kunci")
    caesar_shift = st.number_input("Caesar Shift", value=3)
    vigenere_key = st.text_input("Vigenere Key (string)")
    stream_seed = st.number_input("Stream Cipher Seed (integer)", value=9)
    des_key = st.text_input("DES Key (8 karakter)")

    if st.button("Proses"):
        if len(des_key) != 8:
            st.error("Key DES harus 8 karakter!")
        else:
            result = text

            # ===== ENCRYPTION PIPELINE =====
            if mode == "Enkripsi":
                # Caesar
                result = caesar_cipher(result, caesar_shift)
                st.info(f"Hasil Caesar: {result}")

                # Vigenere
                if vigenere_key:
                    result = vigenere_encrypt(result, vigenere_key)
                    st.info(f"Hasil Vigenere: {result}")

                # Stream Cipher
                def int_to_bits(n, width=8):
                    return [(n >> i) & 1 for i in range(width-1, -1, -1)]
                seed = int_to_bits(int(stream_seed), width=8)
                taps = [0, len(seed)-1]
                result = stream_encrypt(result, seed, taps)
                st.info(f"Hasil Stream: {result}")

                # DES
                cipher_bytes = des_encrypt_ecb(result.encode(), des_key.encode())
                result = base64.b64encode(cipher_bytes).decode()
                st.info(f"Hasil DES: {result}")

            # ===== DECRYPTION PIPELINE =====
            else:
                try:
                    # DES
                    cipher_bytes = base64.b64decode(result.encode())
                    plain_bytes = des_decrypt_ecb(cipher_bytes, des_key.encode())
                    result = plain_bytes.decode()
                    st.info(f"Hasil DES: {result}")

                    # Stream Cipher
                    def int_to_bits(n, width=8):
                        return [(n >> i) & 1 for i in range(width-1, -1, -1)]
                    seed = int_to_bits(int(stream_seed), width=8)
                    taps = [0, len(seed)-1]
                    cipher_bits = [int(b) for b in result.strip()]
                    result = stream_decrypt(cipher_bits, seed, taps)
                    st.info(f"Hasil Stream: {result}")

                    # Vigenere
                    if vigenere_key:
                        result = vigenere_decrypt(result, vigenere_key)
                        st.info(f"Hasil Vigenere: {result}")

                    # Caesar
                    result = caesar_cipher(result, -caesar_shift)
                    st.info(f"Hasil Caesar: {result}")

                except Exception as e:
                    st.error(f"Error during decryption: {e}")

            st.success("Final Result:")
            st.code(result)
