from prettytable import PrettyTable
import numpy as np
from scipy.integrate import quad

# Функция распределения
def f(x):
    return 3 / 14 * np.sqrt(x)

# Интервал
a, b = 1, 4

# Число точек для аппроксимации
N = int(input("Введите число N: "))

# Вычисление математического ожидания
Mx, _ = quad(lambda x: x * f(x), a, b)

# Вычисление дисперсии
Dx, _ = quad(lambda x: (x - Mx)**2 * f(x), a, b)

#вычисление погрешности
m = np.mean(np.random.uniform(a, b, size=N))
g = np.var(np.random.uniform(a, b, size=N))

# Вычисление погрешностей
D1 = abs(Mx - m)
D2 = abs(Dx - g)

# Создание таблицы
mytable = PrettyTable()
mytable.field_names = ["N", "Mx", "m", "D1", "Dx", "g", "D2"]

# Заполнение таблицы
mytable.add_row([N, round(Mx, 4), round(m, 4), round(D1, 4), round(Dx, 4), round(g, 4), round(D2, 4)])

# Вывод таблицы
print(mytable)
