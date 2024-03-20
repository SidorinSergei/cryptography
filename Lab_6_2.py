from sympy import mod_inverse

# Параметры эллиптической кривой E751(-1,1)
a = -1
b = 1
p = 751  # модуль кривой

# Генерирующая точка G(-1,1)
G = (-1, 1)

# Секретный ключ
k = 25

# Шифрованный текст
cipher_text = [
    ((425, 663), (651, 191)), ((188, 93), (177, 562)), ((286, 136), (603, 562)),
    ((440, 539), (588, 707)), ((72, 254), (269, 187)), ((56, 419), (49, 568)),
    ((16, 416), (426, 662)), ((425, 663), (557, 28)), ((138, 93), (149, 97)),
    ((179, 275), (711, 341))
]


# Функция сложения двух точек на эллиптической кривой
def add_points(P, Q, a, p):
    # Случай когда точки различны
    if P != Q:
        lambda_numerator = Q[1] - P[1]
        lambda_denominator = Q[0] - P[0]
    # Случай когда точки совпадают
    else:
        lambda_numerator = (3 * P[0] ** 2 + a)
        lambda_denominator = (2 * P[1])

    # Вычисляем λ (lambda)
    lambda_value = (lambda_numerator * mod_inverse(lambda_denominator, p)) % p

    # Вычисляем координаты новой точки
    x3 = (lambda_value ** 2 - P[0] - Q[0]) % p
    y3 = (lambda_value * (P[0] - x3) - P[1]) % p
    return (x3, y3)


# Функция умножения точки на число
def mul_point(P, n, a, p):
    Q = P
    R = None  # Нейтральный элемент для сложения точек на кривой
    while n > 0:
        # Если n нечетное, добавляем текущую точку Q к результату
        if n % 2 == 1:
            if R is None:
                R = Q
            else:
                R = add_points(R, Q, a, p)
        # Удваиваем точку Q
        Q = add_points(Q, Q, a, p)
        n = n // 2
    return R


# Дешифрование каждой пары точек
decrypted_text_points = []
for C1, C2 in cipher_text:
    # Вычисляем k*C1
    kC1 = mul_point(C1, k, a, p)
    # Инвертируем y координату для kC1
    kC1_inv = (kC1[0], -kC1[1] % p)
    # Получаем исходную точку P
    P = add_points(C2, kC1_inv, a, p)
    decrypted_text_points.append(P)

decrypted_text_points
