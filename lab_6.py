from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)


def calculate_delta(chastota, num_intervals):
    total_observations = sum(chastota)
    normalized_chast = [freq / total_observations for freq in chastota]

    p = 0.2

    delta = sum((normalized_freq - p) ** 2 / p
                for normalized_freq in normalized_chast)

    return delta


def make_fig(nums, M, N):
    fig, ax = plt.subplots()

    # Создаем исходный гистограмм
    n, bins, patches = ax.hist(nums, bins=M, color='green', alpha=0.75)

    # Получаем высоты столбцов и их положение
    heights = n
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Вычисляем новые значения для оси Y
    new_heights = (heights / np.sum(heights)) / (bins[1] - bins[0])
    delta_value = calculate_delta(heights, 5)


    # Создаем новый график с новыми значениями
    ax.clear()  # Очищаем предыдущий график
    ax.bar(bin_centers, new_heights, width=bins[1] - bins[0], color='green', alpha=0.75)

    plt.xlabel('Интервал')
    plt.ylabel('Нормированная частота')
    plt.title('Равномерное распределение')
    plt.grid(True)

    # Добавляем текст с значением delta
    ax.text(0.05, 0.95, f'delta = {delta_value:.4f}', transform=ax.transAxes,
            fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    plt.close(fig)

    return f'data:image/png;base64,{img_str}'


@app.route('/')
def index():
    return render_template('index.html', need_lambda=False)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        a = float(request.form['a'])
        b = float(request.form['b'])
        N = int(request.form['n'])

        M = 5

        # Фиксированное зерно для воспроизводимости
        np.random.seed(42)

        Mx = (a + b) / 2
        Dx = ((b - a) ** 2) / 12
        r = np.random.uniform(0, 1, size=N)
        all_x = []
        for ri in r:
            xi = a + (ri * (b - a))
            all_x.append(xi)

        # вычисление погрешности
        m = sum(all_x) / N
        g = sum([xi ** 2 for xi in all_x]) / N - m ** 2

        D1 = abs(Mx - m)
        D2 = abs(Dx - g)

        result = list(sorted([round(x, 4) for x in all_x[:20]]))
        #result = [0,1,2,0,1,3,0,0,1,1,2,0,1,0,1,2,3,0,0,1]
        plot_url = make_fig(result, M, N)
        type = "Равномерное распределение"
        return render_template('result.html', result=result, d1=D1, d2=D2, a=a, b=b, N=N, type=type, plot_url=plot_url)
    except ValueError:
        return render_template("Ошибка: неверный формат входных данных.")


if __name__ == '__main__':
    app.run(debug=True, port=5555)
