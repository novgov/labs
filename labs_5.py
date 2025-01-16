from flask import Flask, render_template, request
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)


def make_fig(nums):
    fig, ax = plt.subplots(figsize=(5, 3))
    with plt.style.context('default'):
        ax.hist(nums, bins=10, alpha=0.7, color='skyblue', edgecolor='black')

        ax.set_title('Гистограмма')
        ax.set_xlabel('Значение')
        ax.set_ylabel('Частота')

        ax.grid(True, linestyle='--', alpha=0.7)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Закрытие фигуры
    plt.close(fig)

    return f'data:image/png;base64,{img_str}'

@app.route('/')
def index():
    return render_template('index_for_5.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        m = float(request.form['m'])
        si = float(request.form['si'])
        N = int(request.form['n'])

        Mx = 0
        Dx = 1
        r = np.random.uniform(0, 1, size=N)
        all_x = []
        for ri in r:
            xi = 0
            for j in range(12):
                xi += ri

            all_x.append((si*xi)+m)

        m = sum(all_x) / N
        g = sum([xi ** 2 for xi in all_x]) / N - m ** 2

        D1 = abs(Mx - m)
        D2 = abs(Dx - g)

        result = [round(x, 4) for x in all_x[:20]]
        type = "Нормальное распределение"

        plot_url = make_fig(result)
        return render_template('result_for_5.html', result=result, d1=D1, d2=D2, m=m, si=si, N=N, type=type, plot_url=plot_url)
    except ValueError:
        return render_template("error.html", error="Ошибка: неверный формат входных данных.")


if __name__ == '__main__':
    app.run(debug=True)
