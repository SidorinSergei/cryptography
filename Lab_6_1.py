# Определяем функции для работы с эллиптическими кривыми

def inv_mod_p(x, p):
    """Вычисление обратного элемента по модулю p."""
    return pow(x, p-2, p)

def add_points(P, Q, a, p):
    """Сложение двух точек P и Q на эллиптической кривой."""
    if P == Q:
        lam = (3 * P[0]**2 + a) * inv_mod_p(2 * P[1], p) % p
    else:
        lam = (Q[1] - P[1]) * inv_mod_p(Q[0] - P[0], p) % p
    x3 = (lam**2 - P[0] - Q[0]) % p
    y3 = (lam * (P[0] - x3) - P[1]) % p
    return (x3, y3)

def mul_point(P, k, a, p):
    """Умножение точки P на скаляр k на эллиптической кривой."""
    R = ('inf', 'inf')
    while k:
        if k & 1:
            if R == ('inf', 'inf'):
                R = P
            else:
                R = add_points(R, P, a, p)
        P = add_points(P, P, a, p)
        k >>= 1
    return R

# Данные для шифрования
numerical_representations = {
    'п': (240, 442),
    'р': (243, 87),
    'о': (240, 309),
    'к': (237, 297),
    'у': (247, 485),
    'т': (247, 266),
    'а': (228, 271)
}
public_key = (618, 206)
random_values = [10, 15, 16, 2, 3, 4, 2, 11, 16]

# Параметры эллиптической кривой
a = -1  # a в уравнении кривой
b = 1   # b в уравнении кривой
p = 751 # модуль кривой

# Функция шифрования сообщения
def encrypt_message(message, public_key, G, random_values, a, p):
    encrypted_message = []
    for symbol, k in zip(message, random_values):
        P = numerical_representations[symbol]  # Сообщение P
        C1 = mul_point(G, k, a, p)  # kG
        k_public_key = mul_point(public_key, k, a, p)  # kY
        C2 = add_points(P, k_public_key, a, p)  # P + kY
        encrypted_message.append((C1, C2))
    return encrypted_message

# Текст сообщения
message = 'прокрутка'

# Шифрование сообщения
encrypted_message = encrypt_message(message, public_key, G, random_values, a, p)
encrypted_message
