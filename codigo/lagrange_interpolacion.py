"""
Interpolación polinomial de Lagrange.

Implementación del pseudocódigo de la Figura 18.11 de:
Chapra, S. C. y Canale, R. P. — "Métodos numéricos para ingenieros".

El polinomio de Lagrange se expresa como una combinación lineal de los
valores y[i] ponderados por polinomios base L_i(xi), que valen 1 en x[i]
y 0 en los demás nodos. No requiere construir tabla de coeficientes: se
evalúa directamente en el punto de interés.
"""

import numpy as np


def lagrange(x, y, xi):
    """
    Interpolación polinomial de Lagrange.

    Reproduce la FUNCTION Lagrng de la Figura 18.11 de Chapra.

    Nota sobre nombres: el pseudocódigo usa 'x' tanto para el arreglo de
    datos como para el punto de evaluación, lo cual es ambiguo. Aquí se
    usan nombres distintos: 'x' es el arreglo de datos y 'xi' el punto a
    interpolar.

    Parámetros
    ----------
    x : array_like
        Abscisas de los n+1 puntos de datos conocidos.
    y : array_like
        Ordenadas de los n+1 puntos de datos conocidos.
    xi : float
        Valor en el que se desea interpolar.

    Retorna
    -------
    float
        Estimación interpolada f(xi) (el 'sum' del pseudocódigo).

    Notas
    -----
    El pseudocódigo define 'n' como el grado del polinomio; con n+1 puntos
    de datos se tiene n = len(x) - 1. En Python se recorre range(len(x)).
    """
    # Convertimos a arreglos de numpy de punto flotante.
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    npts = len(x)   # número de puntos = n+1 en el pseudocódigo

    # Acumulador de la suma de los términos y[i] * L_i(xi).
    suma = 0.0

    # Bucle externo: recorre cada punto de datos i.
    # Pseudocódigo: DOFOR i = 0, n
    for i in range(npts):          # i = 0 .. n
        # 'product' arranca en y[i] y se multiplica por el polinomio base.
        product = y[i]

        # Bucle interno: construye el polinomio base L_i(xi).
        # Pseudocódigo: DOFOR j = 0, n ; IF i != j
        for j in range(npts):      # j = 0 .. n
            if i != j:             # se omite el factor j = i
                product = product * (xi - x[j]) / (x[i] - x[j])

        # Se acumula el término correspondiente al punto i.
        suma = suma + product

    return suma


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Ejemplo clásico de Chapra: estimar ln(2) por interpolación de
    # Lagrange usando tres puntos (grado 2) y evaluando en xi = 2.
    # ------------------------------------------------------------------
    x = [1, 4, 6]
    y = [0, 1.386294, 1.791759]
    xi = 2

    resultado = lagrange(x, y, xi)
    valor_real = np.log(2)  # ln(2) para comparar

    # Error verdadero relativo porcentual respecto a ln(2).
    et = abs((valor_real - resultado) / valor_real) * 100

    print("Interpolación polinomial de Lagrange")
    print(f"Puntos:  x = {x}")
    print(f"         y = {y}")
    print(f"Evaluando en xi = {xi}\n")
    print(f"Estimación f({xi})   = {resultado:.6f}")
    print(f"Valor real ln(2)   = {valor_real:.6f}")
    print(f"Error verdadero    = {et:.3f}%")

    # ------------------------------------------------------------------
    # Gráfica opcional: puntos de datos y polinomio interpolante.
    # ------------------------------------------------------------------
    try:
        import matplotlib.pyplot as plt

        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)

        # Malla fina: evaluamos el polinomio de Lagrange en muchos puntos
        # del intervalo para dibujar la curva.
        xs = np.linspace(x_arr.min(), x_arr.max(), 300)
        ys = np.array([lagrange(x_arr, y_arr, xv) for xv in xs])

        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, label="Polinomio de Lagrange (grado 2)", color="C0")
        plt.scatter(x_arr, y_arr, color="C3", zorder=5, label="Puntos de datos")
        plt.scatter([xi], [resultado], color="C2", zorder=6,
                    label=f"Interpolación en xi={xi}")
        # Referencia: función real ln(x).
        plt.plot(xs, np.log(xs), "--", color="gray", label="ln(x) (real)")

        plt.title("Interpolación polinomial de Lagrange")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("\n(matplotlib no está instalado; se omite la gráfica.)")
