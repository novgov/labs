import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


# Определение функции плотности и ее обратной
def f(x):
    return 3 / 14 * np.sqrt(x)


def inv_f(p):
    return (p * 14 / 3) ** 2 - 1


def run():
    # Генерация N=90 значений случайной величины
    N = 90
    X = np.array([inv_f(np.random.uniform(0, 1)) for _ in range(N)])

    # Вычисление точных значений матожидания и дисперсии
    mu_exact = 4 * (14 / 3) ** 2 / 5 - 1
    sigma_exact = 4 / (45 * (14 / 3) ** 2)

    print("\nТочное математическое ожидание:", mu_exact)
    print("Оценка математического ожидания:", np.mean(X))
    print("Точная дисперсия:", sigma_exact)
    print("Оценка дисперсии:", np.std(X, ddof=1))

    # Создание фигуры и двух подграфиков
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 8))

    # Подграфик для функции и точек распределения
    x = np.linspace(0, X.max(), 100)
    y = f(x)
    ax1.plot(x, y, color='red', label='Линия плотности')

    ax1.scatter(X, np.zeros_like(X), color='blue', alpha=0.5, label='Точки распределения')

    ax1.axvline(x=mu_exact, color='green', linestyle='--', label='Математическое ожидание')
    ax1.axvline(x=np.mean(X), color='orange', linestyle=':', label='Оценка матожидания')
    ax1.axvline(x=mu_exact + sigma_exact, color='purple', linestyle='--', label='Дисперсия')
    ax1.axvline(x=mu_exact - sigma_exact, color='purple', linestyle='--')

    ax1.set_title("Функция распределения и точки распределения")
    ax1.set_xlabel('Значения случайной величины')
    ax1.set_ylabel('Плотность распределения')
    ax1.legend()


    plt.show()


if __name__ == "__main__":
    run()
