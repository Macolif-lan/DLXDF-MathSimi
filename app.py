from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import sympy as sp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    function_str = 'exp(x)'
    a, b, n = 0, 1, 10

    if request.method == 'POST':
        function_str = request.form['function']
        a = float(request.form['a'])
        b = float(request.form['b'])
        n = int(request.form['n'])

        # Define the function to integrate
        x = sp.symbols('x')
        f = sp.sympify(function_str)
        f_np = sp.lambdify(x, f, 'numpy')

        x_vals = np.linspace(a, b, n+1)
        y_vals = f_np(x_vals)

        # Rectangle method
        dx = (b - a) / n
        rectangle_integral = np.sum(y_vals[:-1]) * dx

        # Trapezoidal method
        trapezoidal_integral = (dx / 2) * np.sum(y_vals[:-1] + y_vals[1:])

        # Symbolic integral and its derivation
        symbolic_integral = sp.integrate(f, (x, a, b))
        integral_derivation = sp.integrate(f, x)

        # Create plots for Rectangle and Trapezoidal methods
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, 'r', label='Function')

        # Plot rectangles
        for i in range(n):
            ax.add_patch(plt.Rectangle((x_vals[i], 0), dx, y_vals[i], edgecolor='blue', facecolor='blue', alpha=0.3))
        ax.set_title('Rectangle Method')
        ax.legend()
        img = io.BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        rectangle_plot = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, 'r', label='Function')

        # Plot trapezoids
        for i in range(n):
            ax.fill_between([x_vals[i], x_vals[i+1]], 0, [y_vals[i], y_vals[i+1]], edgecolor='green', facecolor='yellow', alpha=0.3)
        ax.set_title('Trapezoidal Method')
        ax.legend()
        img = io.BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        trapezoidal_plot = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)

        return render_template('index.html', rectangle_integral=rectangle_integral,
                               trapezoidal_integral=trapezoidal_integral,
                               symbolic_integral=symbolic_integral,
                               integral_derivation=integral_derivation,
                               rectangle_plot=rectangle_plot,
                               trapezoidal_plot=trapezoidal_plot,
                               function_str=function_str,
                               a=a, b=b, n=n)

    return render_template('index.html', rectangle_integral=None, trapezoidal_integral=None,
                           symbolic_integral=None, integral_derivation=None,
                           rectangle_plot=None, trapezoidal_plot=None,
                           function_str=function_str, a=a, b=b, n=n)

if __name__ == '__main__':
    app.run(debug=True)
