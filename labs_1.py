from prettytable import PrettyTable
import numpy as np
from scipy.integrate import quad

m1, m2, m3 = [0 for _ in range(3)]
x1, x2, x3 = [-43, 15, 33]
p1, p2, p3 = [0.4, 0.2, 0.4]
xs = [33, -43, 15]
ps = [0.4, 0.4, 0.2]
N = int(input("введите N"))
nums = np.random.uniform(0, 1, size=N)
for num in nums:
    if num >= 0 and num < p1:
        m1 += 1
    if num >= p1 and num < p1+p2:
        m2 += 1
    if num > p1+p2 and num <= 1:
        m3 += 1
mx = 0
for x, p in zip(xs, ps):
    mx += x*p
dx = 0
for x, p in zip(xs, ps):
    dx += (x**2)*p
dx = dx - (mx**2)

m = ((m1 * x1) + (m2 * x2) + (m3 * x3))/N
g = 1 / (N - 1) * ((m1 * (x1 ** 2)) + (m2 * (x2 ** 2)) + (m3 * (x3 ** 2))) - m ** 2
D1 = (mx - m)
D2 = (dx - g)

mytable = PrettyTable()
mytable.field_names = ["N", "Mx", "m", "D1", "Dx", "g", "D2"]

# Заполнение таблицы
mytable.add_row([N, round(mx, 4), round(m, 4), round(D1, 4), round(dx, 4), round(g, 4), round(D2, 4)])

# Вывод таблицы
print(mytable)



