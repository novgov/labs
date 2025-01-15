from flask import Flask, render_template, request
import numpy as np
import math

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        a = float(request.form['a'])
        b = float(request.form['b'])
        l = float(request.form['l'])
        N = int(request.form['n'])

        result = list(range(20))

        Mx = 1 / l
        Dx = 1 / l**2
        r = np.random.uniform(0, 1, size=N)
        all_x = []
        for ri in r:
            xi = - 1/l * math.log(1 - ri)
            all_x.append(xi)
            # вычисление погрешности
        m = sum(all_x) / N
        g = sum([xi ** 2 for xi in all_x]) / N - m ** 2

        D1 = abs(Mx - m)
        D2 = abs(Dx - g)

        result = [round(x, 4) for x in all_x[:20]]
        type = "Показательное распределение"
        return render_template('result.html', result=result, d1=D1, d2=D2, a=a, b=b, N=N, type=type)
    except ValueError:
        return render_template("Ошибка: неверный формат входных данных.")


if __name__ == '__main__':
    app.run(debug=True)
