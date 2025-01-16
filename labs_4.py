from flask import Flask, render_template, request
import numpy as np
import math
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
    return render_template('index.html', need_lambda=True)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        a = float(request.form['a'])
        b = float(request.form['b'])
        l = float(request.form['l'])
        N = int(request.form['n'])

        Mx = 1 / l
        Dx = 1 / l**2
        r = np.random.uniform(0, 1, size=N)
        all_x = []
        for ri in r:
            xi = - 1/l * math.log(1 - ri)
            all_x.append(xi)

        m = sum(all_x) / N
        g = sum([xi ** 2 for xi in all_x]) / N - m ** 2

        D1 = abs(Mx - m)
        D2 = abs(Dx - g)

        result = [round(x, 4) for x in all_x[:20]]
        type = "Нормальное распределение"

        plot_url = make_fig(result)
        return render_template('result.html', result=result, d1=D1, d2=D2, a=a, b=b, N=N, type=type, plot_url=plot_url, l=l)
    except ValueError:
        return render_template("error.html", error="Ошибка: неверный формат входных данных.")

if __name__ == '__main__':
    app.run(debug=True)
