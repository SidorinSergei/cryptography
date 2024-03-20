# Task 8.1.1 - Генерация линейной конгруэнтной последовательности
def linear_congruential_generator(a, c, m, x0, n):
    """ Генерирует линейную конгруэнтную последовательность.

    Args:
    a (int): Множитель.
    c (int): Приращение.
    m (int): Модуль.
    x0 (int): Начальное значение или зерно.
    n (int): Количество элементов для генерации.

    Returns:
    list: Список, содержащий первые n элементов последовательности.
    """
    sequence = [x0]
    for _ in range(1, n):
        # Вычисление следующего элемента последовательности по формуле линейного конгруэнтного метода
        x_next = (a * sequence[-1] + c) % m
        sequence.append(x_next)
    return sequence


# Task 8.1.2 - Генерация линейной конгруэнтной последовательности v2
def linear_congruential_generator_v2(a, c, m, x0, n):
    """ Генерирует линейную конгруэнтную последовательность.

    Args:
    a (int): Множитель.
    c (int): Приращение.
    m (int): Модуль.
    x0 (int): Начальное значение или зерно.
    n (int): Количество элементов для генерации.

    Returns:
    list: Список, содержащий первые n элементов последовательности.
    """
    sequence = [x0]
    for _ in range(1, n):
        # Вычисление следующего элемента последовательности по формуле линейного конгруэнтного метода
        x_next = (a * sequence[-1] + c) % m
        sequence.append(x_next)
    return sequence


# Task 8.2.1 - Генерация линейной конгруэнтной последовательности с заданным периодом
def linear_congruential_generator(m, a, c, X0, length):
    sequence = [X0]
    for _ in range(length - 1):
        # Вычисление следующего элемента последовательности по формуле линейного конгруэнтного метода
        X_next = (a * sequence[-1] + c) % m
        sequence.append(X_next)
    return sequence


# Task 8.2.2 - Поиск параметров для заданного периода T
def linear_congruential_generator_find_params(T):
    modulus = T
    possible_params = []
    for a in range(1, modulus):
        for c in range(1, modulus):
            # Проверка параметров на соответствие заданному периоду
            sequence = linear_congruential_generator(modulus, a, c, 0, modulus)
            if len(set(sequence)) == modulus:
                possible_params.append((a, c))

    if possible_params:
        print(f"Существуют параметры для периода T={T}:")
        for a, c in possible_params:
            print(f"a = {a}, c = {c}")
    else:
        print(f"Параметры не найдены для периода T={T}")


# Task 8.3.1 - Генерация последовательности задержанных чисел Фибоначчи
def delayed_fibonacci_generator(delay):
    a, b = 0, 1
    sequence = []
    for _ in range(delay):
        sequence.append(a)
        # Вычисление следующего числа Фибоначчи
        a, b = b, a + b
    while True:
        # Возврат последнего числа Фибоначчи из последовательности
        yield sequence[-1]
        # Добавление следующего числа Фибоначчи в последовательность
        sequence.append(a)
        a, b = b, a + b
        # Удаление первого числа Фибоначчи из последовательности
        sequence.pop(0)


# Task 8.3.2 - Генерация последовательности задержанных чисел Фибоначчи над GF(2^n)
from sympy import *


def delayed_fibonacci_GF2n_generator(delay, n):
    x = symbols('x')
    field = GF(2 ** n)
    a = field(0)
    b = field(1)
    sequence = []
    for _ in range(delay):
        sequence.append(a)
        # Вычисление следующего числа Фибоначчи над GF(2^n)
        a, b = b, a + b
    while True:
        # Возврат последнего числа Фибоначчи из последовательности
        yield sequence[-1]
        # Добавление следующего числа Фибоначчи в последовательность
        sequence.append(a)
        a, b = b, a + b
        # Удаление первого числа Фибоначчи из последовательности
        sequence.pop(0)


# Task 8.4 - Генерация последовательности методом Блюма-Блюма-Шуба
def blum_blum_shub_generator(p, q, seed, length):
    n = p * q
    x = seed
    sequence = []
    for _ in range(length):
        # Генерация следующего бита последовательности методом Блюма-Блюма-Шуба
        x = (x * x) % n
        sequence.append(x % 2)
    return sequence


# Task 8.5 - Нахождение периода для заданных регистров линейной обратной связи
def linear_feedback_shift_register(F, initial_state):
    state = initial_state
    period = 0
    visited_states = set()

    while True:
        visited_states.add(state)
        # Сдвиг состояния на 1 бит
        state = (state << 1) & ((1 << len(F)) - 1)
        # Применение обратной связи
        feedback_bit = sum(state & F[i] for i in range(len(F))) % 2
        state |= feedback_bit
        period += 1

        if state in visited_states:
            break

    return period


# Task 8.7 - Проверка на неприводимость и примитивность полинома
from sympy import symbols, factor, GF

x = symbols('x')


def is_irreducible(poly):
    factors = factor(poly)
    # Полином неприводим, если у него только один множитель степени 1
    return len(factors.args) == 1 and factors.args[0][1] == 1


def is_primitive(poly, n):
    field = GF(2 ** n)
    x = symbols('x')
    min_poly = field.minpoly(x)
    # Проверка, является ли заданный полином примитивным над GF(2^n)
    return poly == min_poly


# Task 8.8 - Нахождение периода для заданных последовательностей
def find_period(sequence):
    period = 1
    for i in range(1, len(sequence)):
        # Проверяем, повторяется ли последовательность
        if sequence[:i] == sequence[i:2 * i]:
            period = i
            break
    return period


# Task 8.1.1 - Generate linear congruential sequence
def task_8_1_1():
    # Parameters
    a = 4
    c = 7
    m = 10
    x0 = 1
    n = 10
    # Generate the sequence
    lc_sequence = linear_congruential_generator(a, c, m, x0, n)
    return lc_sequence

# Task 8.1.2 - Generate linear congruential sequence v2
def task_8_1_2():
    # Parameters
    a_812 = 4
    c_812 = 5
    m_812 = 9
    x0_812 = 1
    n_812 = 10
    # Generate the sequence
    lc_sequence_812 = linear_congruential_generator_v2(a_812, c_812, m_812, x0_812, n_812)
    return lc_sequence_812

# Task 8.2.1 - Generate linear congruential sequence with given period
def task_8_2_1():
    # Examples with period 8
    sequences = []
    # Example 1
    m1, a1, c1, X01, length1 = 11, 3, 2, 7, 8
    sequences.append(linear_congruential_generator(m1, a1, c1, X01, length1))
    # Example 2
    m2, a2, c2, X02, length2 = 17, 5, 3, 11, 8
    sequences.append(linear_congruential_generator(m2, a2, c2, X02, length2))
    # Example 3
    m3, a3, c3, X03, length3 = 13, 4, 7, 5, 8
    sequences.append(linear_congruential_generator(m3, a3, c3, X03, length3))
    return sequences

# Task 8.2.2 - Find parameters for given period T
def task_8_2_2(T):
    linear_congruential_generator_find_params(T)

# Task 8.3.1 - Generate delayed Fibonacci sequence
def task_8_3_1():
    # Example usage
    gen = delayed_fibonacci_generator(3)
    sequence = [next(gen) for _ in range(10)]
    return sequence

# Task 8.3.2 - Generate delayed Fibonacci sequence over GF(2^n)
def task_8_3_2():
    # Example usage
    gen_GF2n = delayed_fibonacci_GF2n_generator(3, 4)
    sequence_GF2n = [next(gen_GF2n) for _ in range(10)]
    return sequence_GF2n

# Task 8.4 - Generate Blum-Blum-Shub sequence
def task_8_4():
    # Example usage
    p = 11
    q = 19
    seed = 3
    length = 20
    bbs_sequence = blum_blum_shub_generator(p, q, seed, length)
    return bbs_sequence

# Task 8.5 - Find periods for given linear feedback shift registers
def task_8_5():
    # Examples for tasks 8.5.1 and 8.5.2
    periods = []
    # Example 1
    F1 = [1, 1, 0, 0, 1]
    initial_state1 = 0b1010
    periods.append(linear_feedback_shift_register(F1, initial_state1))
    # Example 2
    F2 = [1, 0, 0, 1, 1]
    initial_state2 = 0b10101
    periods.append(linear_feedback_shift_register(F2, initial_state2))
    return periods

# Task 8.7 - Check irreducibility and primitivity of a polynomial
def task_8_7():
    # Given polynomial
    f = x**7 + x**4 + 1
    # Check for irreducibility
    is_irreducible_result = is_irreducible(f)
    # Check for primitivity (assuming the polynomial is irreducible)
    if is_irreducible_result:
        n = 7
        is_primitive_result = is_primitive(f, n)
    else:
        is_primitive_result = False
    return is_irreducible_result, is_primitive_result

# Task 8.8 - Find periods for given sequences
def task_8_8():
    # Sequences
    sequences = [
        "1110000101011001110000101011",
        "1010110101011010101101010110",
        "0000011101011100000011101011",
        "0100100001111100100100001111",
        "0011010111100010011010111100"
    ]
    #лучшая 4
    # Find period for each sequence
    periods = [find_period(sequence) for sequence in sequences]
    return periods

print(task_8_8())
