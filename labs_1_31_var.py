import numpy as np


def generate_random_variable(N, x_values, probabilities):
    cum_prob = np.cumsum(probabilities)
    uniform_rvs = np.random.uniform(0, 1, size=N)
    rvs = np.searchsorted(cum_prob, uniform_rvs)
    return x_values[rvs]


def run():
    # Заданные параметры
    N = 90
    x_values = np.array([33, -43, 15])
    probabilities = np.array([0.4, 0.4, 0.2])

    # Генерируем случайные числа
    generated_rvs = generate_random_variable(N, x_values, probabilities)

    # Выводим q первых значений
    # q = 12
    # print(f"Первые {q} значений:")
    # print(generated_rvs[:q])

    # Рассчитываем точные значения
    exact_mean = np.sum(x_values * probabilities)
    exact_variance = np.sum((x_values ** 2) * probabilities) - exact_mean ** 2
    print(f"\nТочное математическое ожидание: {exact_mean}")
    print(f"Точная дисперсия: {exact_variance}")

    # Рассчитываем оценки
    estimated_mean = np.mean(generated_rvs)
    estimated_variance = np.var(generated_rvs, ddof=0)
    print(f"\nОценка математического ожидания: {estimated_mean}")
    print(f"Оценка дисперсии: {estimated_variance}")


if __name__ == "__main__":
    run()
    