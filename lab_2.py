class ModPower:
    def __init__(self, mod):
        self.mod = mod

    def add_mod(self, a, b):
        """Сложение по модулю."""
        return (a + b) % self.mod

    def mul_mod(self, a, b):
        """Умножение по модулю."""
        return (a * b) % self.mod

    def pow_mod(self, a, exponent):
        """Возведение в степень по модулю, используя малую теорему Ферма для положительных
        и теорему Эйлера для отрицательных степеней."""
        if exponent > 0:
            return self.positive_pow_mod(a, exponent)
        elif exponent < 0:
            return self.negative_pow_mod(a, exponent)
        else:
            # Любое число в степени 0 равно 1
            return 1

    def positive_pow_mod(self, a, exponent):
        """Возведение в положительную степень по модулю, используя малую теорему Ферма."""
        return pow(a, exponent, self.mod)

    def negative_pow_mod(self, a, exponent):
        """Возведение в отрицательную степень по модулю, используя теорему Эйлера."""
        # Обратный элемент по модулю, взаимно простой с модулем
        inv_a = pow(a, self.phi(self.mod) - 1, self.mod)
        # Возведение обратного элемента в абсолютное значение отрицательной степени
        return pow(inv_a, -exponent, self.mod)

    def phi(self, n):
        """Вычисление функции Эйлера."""
        result = n   # Начальное значение равно n
        p = 2
        while p * p <= n:
            # Проверяем, является ли p делителем n
            if n % p == 0:
                # Если да, то учитываем этот делитель
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        # Если n остался простым числом больше 2
        if n > 1:
            result -= result // n
        return result

# Пример использования
mod_power = ModPower(17) # Выбираем модуль 17 для примера
# Вычисляем 3 в степени 4 по модулю 17 (положительная степень)
positive_example = mod_power.pow_mod(3, 4)
# Вычисляем 3 в степени -4 по модулю 17 (отрицательная степень)
negative_example = mod_power.pow_mod(3, -4)

positive_example, negative_example
