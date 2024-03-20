from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.exceptions import InvalidSignature
import os

"""
ECDSA (Elliptic Curve Digital Signature Algorithm) - это алгоритм цифровой подписи, который использует 
математические свойства эллиптических кривых для создания более безопасных и эффективных криптографических ключей.

Алгоритм ECDSA выполняет три основные операции: генерация ключей, подпись сообщения и верификация подписи.

1. Генерация ключей: Пользователь генерирует пару ключей (публичный и приватный) на основе выбранной эллиптической кривой. 
Приватный ключ - это случайное число, а публичный ключ - это точка на эллиптической кривой, полученная в результате умножения 
генераторной точки кривой на приватный ключ.

2. Подпись сообщения: Для создания подписи алгоритм использует приватный ключ и хеш сообщения. Процесс включает в себя 
генерацию случайной точки на кривой и выполнение ряда математических операций, основанных на приватном ключе и хеше сообщения, 
для получения подписи. Подпись состоит из двух компонентов, обычно обозначаемых как r и s.

3. Верификация подписи: Проверка подписи осуществляется с использованием публичного ключа, хеша сообщения и подписи. 
Алгоритм проверяет, соответствует ли подпись сообщению и указанному публичному ключу. Если проверка проходит успешно, 
подпись считается действительной, что подтверждает, что сообщение было подписано владельцем приватного ключа.

В приведенном ниже коде мы демонстрируем пример использования ECDSA для подписания файла и проверки подписи. 
Мы используем библиотеку `cryptography`, которая предоставляет инструменты для работы с криптографией на Python.
"""

# Генерируем ключевую пару ECDSA
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Пример файла для подписи
file_path = "example.txt"

def sign_file(file_path, private_key):
    """
    Подписывает файл, используя приватный ключ ECDSA.
    :param file_path: Путь к файлу, который нужно подписать.
    :param private_key: Приватный ключ ECDSA.
    :return: Подпись в виде байтов.
    """
    with open(file_path, "rb") as f:
        file_data = f.read()
    signature = private_key.sign(
        file_data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_signature(file_path, signature, public_key):
    """
    Проверяет подпись файла, используя публичный ключ ECDSA.
    :param file_path: Путь к файлу, подпись которого проверяется.
    :param signature: Подпись в виде байтов.
    :param public_key: Публичный ключ ECDSA.
    :return: Boolean значение, указывающее, прошла ли проверка успешно.
    """
    with open(file_path, "rb") as f:
        file_data = f.read()

    try:
        # Проверяем подпись
        public_key.verify(
            signature,
            file_data,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False


# Генерируем ключевую пару ECDSA
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Пример файла для подписи
file_path = "example.txt"

# Подписываем файл
signature = sign_file(file_path, private_key)
print(f"Подпись создана: {signature}")

# Проверяем подпись
verification_result = verify_signature(file_path, signature, public_key)
print(f"Результат проверки подписи: {'подпись верна' if verification_result else 'подпись неверна'}")
