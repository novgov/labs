from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
from scipy.stats import norm
matplotlib.use('Agg')

app = Flask(__name__)


def calculate_delta(chastota, N):
    total_observations = sum(chastota)
    normalized_chast = [freq / total_observations for freq in chastota]
    ps = [0.043, 0.137, 0.34, 0.34, 0.137, 0.043]
    # Ожидаемые частоты на основе нормального распределения
    delta = 0
    for i, p in enumerate(ps):
        delta += ((chastota[i] - sum(chastota)*p) ** 2 / (sum(chastota)*p))

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
    delta_value = calculate_delta(heights, N=N)


    # Создаем новый график с новыми значениями
    ax.clear()  # Очищаем предыдущий график
    ax.bar(bin_centers, new_heights, width=bins[1] - bins[0], color='green', alpha=0.75)

    plt.xlabel('Интервал')
    plt.ylabel('Нормированная частота')
    plt.title('Нормальное распределение')
    plt.grid(True)

    # Добавляем текст с значением delta
    ax.text(0.10, 0.95, f'delta = {delta_value:.4f}', transform=ax.transAxes,
            fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    plt.close(fig)

    return f'data:image/png;base64,{img_str}'


@app.route('/')
def index():
    return render_template('index_for_5.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        M = float(request.form['m'])
        si = float(request.form['si'])
        N = int(request.form['n'])


        all_x = []
        for _ in range(N):
            xi = 0
            for _ in range(12):
                ri = np.random.uniform(0, 1, size=1)[0]
                xi += ri
            xi -= 6

            all_x.append((si*xi) + M)

        m = sum(all_x) / N
        g = sum([xi ** 2 for xi in all_x]) / N - m ** 2

        D1 = abs(M - np.mean(all_x))
        D2 = abs(si - np.std(all_x, ddof=1))

        result = [round(x, 4) for x in all_x[:20]]
        type = "Нормальное распределение"

        plot_url = make_fig(all_x, 6, N=N)
        return render_template('result_for_5.html', result=result, d1=D1, d2=D2, si=si, N=N, type=type, plot_url=plot_url)
    except ValueError:
        return render_template("error.html", error="Ошибка: неверный формат входных данных.")


    except ValueError:
        return render_template("Ошибка: неверный формат входных данных.")


if __name__ == '__main__':
    app.run(debug=True, port=5555)
