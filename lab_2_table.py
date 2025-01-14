from prettytable import PrettyTable
import numpy as np

# Функция распределения
def f(x):
    return ((7*x+1)**2)**(1/3)

# Интервал
a, b = 0, 1

# Число точек для ппроксимации
nums = list(map(int, input("Введите 3 числа N: ").split()))

Mx = 93/35
Dx = 47.3681

# Создание таблицы
table = PrettyTable()
table.field_names = ["N", "Mx", "m", "D1", "Dx", "g", "D2"]

for i in range(len(nums)):
    N = nums[i]
    r = np.random.uniform(0, 1, size=N)

    xi = f(r)

    # вычисление погрешности
    m = sum(xi) / N
    g = 1 / N * sum(xi ** 2) - m ** 2

    # Вычисление погрешностей
    D1 = abs(Mx - m)
    D2 = abs(Dx - g)

    # Заполнение таблицы
    table.add_row([N, np.round(Mx, 4), np.round(m, 4), np.round(D1, 4), np.round(D2, 4), np.round(Dx, 4), np.round(g, 4)])

# Вывод таблицы
print(table)