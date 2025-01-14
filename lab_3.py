from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        a = float(request.form['a'])
        b = float(request.form['b'])
        N = int(request.form['n'])

        result = list(range(20))

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

        result = [round(x, 4) for x in all_x[:20]]

        return render_template('result.html', result=result, d1=D1, d2=D2, a=a, b=b, N=N)
    except ValueError:
        return render_template("Ошибка: неверный формат входных данных.")


if __name__ == '__main__':
    app.run(debug=True)
