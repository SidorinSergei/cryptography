from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import os

# Шаг 1: Генерация ключей RSA и AES
# Создаем пару ключей RSA. Это позволит Алисе зашифровать номер ключа симметричного шифрования (AES)
# и передать его Бобу безопасным образом. Открытый и закрытый ключи RSA будут сохранены в файл для последующего использования.
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Сохраняем открытый и закрытый ключи RSA в файлы
with open("private.pem", "wb") as prv_file:
    prv_file.write(private_key)

with open("public.pem", "wb") as pub_file:
    pub_file.write(public_key)

# Генерация секретного ключа AES. Этот ключ будет использован для шифрования и расшифрования сообщений между Алисой и Бобом.
# Мы выбрали AES в режиме ECB (Electronic Codebook) для демонстрации, хотя этот режим имеет потенциальные уязвимости.
aes_key = os.urandom(16)  # 128 бит

# Шаг 2: Шифрование номера ключа AES с использованием открытого ключа RSA
# Алиса шифрует ключ AES, используя открытый ключ RSA, и передает его Бобу.
public_key_rsa = RSA.import_key(public_key)
cipher_rsa = PKCS1_OAEP.new(public_key_rsa)
encrypted_aes_key = cipher_rsa.encrypt(aes_key)

# Боб будет использовать свой закрытый ключ для расшифровки номера ключа AES.
private_key_rsa = RSA.import_key(private_key)
cipher_rsa = PKCS1_OAEP.new(private_key_rsa)
decrypted_aes_key = cipher_rsa.decrypt(encrypted_aes_key)

# Убеждаемся, что расшифрованный ключ AES совпадает с оригинальным
assert decrypted_aes_key == aes_key, "Ключи AES не совпадают!"

# Шаг 3: Шифрование и расшифрование сообщения с использованием AES
# Алиса шифрует сообщение с использованием ключа AES и отправляет его Бобу.
# Боб расшифровывает сообщение, используя тот же ключ AES.
message = "Привет, Боб! Это сообщение от Алисы.".encode('utf-8')  # Кодировка UTF-8

# Инициализация шифра AES
cipher_aes = AES.new(aes_key, AES.MODE_ECB)

# Шифрование сообщения
encrypted_message = cipher_aes.encrypt(pad(message, AES.block_size))

# Расшифровка сообщения
decrypted_message = unpad(cipher_aes.decrypt(encrypted_message), AES.block_size)

# Вывод зашифрованного и расшифрованного сообщений
print("Зашифрованное сообщение:", encrypted_message)
print("Расшифрованное сообщение:", decrypted_message.decode('utf-8'))
