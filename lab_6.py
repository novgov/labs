from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

def make_fig(nums):
    fig = sns.histplot(nums, bins=5, kde=True)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Закрытие фигуры
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
        plot_url = make_fig(result)
        type = "Показательное распределение"
        return render_template('result.html', result=result, d1=D1, d2=D2, a=a, b=b, N=N, type=type, plot_url=plot_url)
    except ValueError:
        return render_template("Ошибка: неверный формат входных данных.")


if __name__ == '__main__':
    app.run(debug=True)
