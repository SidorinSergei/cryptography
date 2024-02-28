import random
import time
from math import gcd
from functools import reduce  # Импортируем функцию для свертки итерируемого объекта

# Функция для генерации случайных чисел в заданном диапазоне
def generate_random_numbers(count, lower_bound=10_000_001, upper_bound=100_000_000):
    return [random.randint(lower_bound, upper_bound) for _ in range(count)]

# Метод 1: Вычисление функции Эйлера через проверку взаимной простоты
def euler_phi_definition(n):
    count = 0  # Счетчик для чисел, взаимно простых с n
    for k in range(1, n):  # Перебираем числа от 1 до n-1
        if gcd(k, n) == 1:  # Если НОД(k, n) == 1, то числа взаимно просты
            count += 1  # Увеличиваем счетчик
    return count  # Возвращаем количество чисел, взаимно простых с n

# Метод 2: Вычисление функции Эйлера через формулу, используя разложение на простые множители
def prime_factors(n):
    i = 2  # Начальный делитель
    factors = []  # Список для хранения простых множителей
    while i * i <= n:  # Пока квадрат делителя не превысит n
        if n % i:  # Если n не делится на i без остатка
            i += 1  # Переходим к следующему числу
        else:  # Если n делится на i
            n //= i  # Делим n на i
            factors.append(i)  # Добавляем i в список множителей
    if n > 1:  # Если остался множитель больше 1
        factors.append(n)  # Добавляем его в список
    return list(set(factors))  # Возвращаем список уникальных множителей

def euler_phi_formula(n):
    factors = prime_factors(n)  # Получаем простые множители числа n
    # Применяем формулу: φ(n) = n * ∏(1 - 1/p), где p - простые множители n
    result = reduce(lambda x, y: x * (1 - 1/y), factors, n)
    return int(result)  # Возвращаем результат как целое число

# Функция для сравнения эффективности методов
def compare_methods(numbers):
    # Измеряем время выполнения метода по определению
    start_time_def = time.time()
    results_def = [euler_phi_definition(n) for n in numbers]
    end_time_def = time.time()

    # Измеряем время выполнения метода через формулу
    start_time_form = time.time()
    results_form = [euler_phi_formula(n) for n in numbers]
    end_time_form = time.time()

    # Рассчитываем и возвращаем времена выполнения для каждого метода
    execution_time_def = end_time_def - start_time_def
    execution_time_form = end_time_form - start_time_form

    return execution_time_def, execution_time_form, results_def, results_form

numbers = generate_random_numbers(10)
execution_time_def, execution_time_form, results_def, results_form = compare_methods(numbers)

print(f"Время выполнения метода по определению: {execution_time_def} сек.")
print(f"Время выполнения метода через формулу: {execution_time_form} сек.")
print(f"Результаты метода по определению: {results_def}")
print(f"Результаты метода через формулу: {results_form}")
