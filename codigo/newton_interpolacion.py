"""
Interpolación polinomial de Newton por diferencias divididas.

Implementación del pseudocódigo de la Figura 18.8 de:
Chapra, S. C. y Canale, R. P. — "Métodos numéricos para ingenieros".

El método construye una tabla de diferencias divididas finitas y evalúa el
polinomio interpolante de Newton en un punto xi, entregando además la
estimación de cada orden (grado 0..n) y el error aproximado asociado.
"""

import numpy as np


def newt_int(x, y, xi):
    """
    Interpolación polinomial de Newton por diferencias divididas.

    Reproduce la SUBROUTINE NewtInt de la Figura 18.8 de Chapra.

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
    yint : numpy.ndarray
        Estimaciones de la interpolación para cada orden 0..n.
        yint[k] es la estimación con el polinomio de grado k.
        yint[-1] es el resultado final de mayor orden.
    ea : numpy.ndarray
        Error aproximado en cada orden. ea[k] = yint[k+1] - yint[k].
        Tiene n entradas (una menos que yint); la última posición queda
        indefinida para el orden máximo, por lo que se reporta como NaN.

    Notas
    -----
    El pseudocódigo usa índices basados en 0 y define 'n' como el grado
    máximo del polinomio; con n+1 puntos de datos se tiene n = len(x) - 1.
    """
    # Convertimos a arreglos de numpy de punto flotante.
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # np = número de puntos de datos; n = grado máximo del polinomio.
    npts = len(x)          # equivale a n+1 en el pseudocódigo
    n = npts - 1           # grado máximo (el 'n' de la Figura 18.8)

    # ------------------------------------------------------------------
    # Tabla de diferencias divididas: matriz (n+1) x (n+1).
    # Solo se usa la parte triangular superior; el resto queda en cero.
    # ------------------------------------------------------------------
    fdd = np.zeros((npts, npts))

    # Primera columna: las diferencias divididas de orden cero son y[i].
    # Pseudocódigo: DOFOR i = 0, n  ->  fdd[i,0] = y[i]
    for i in range(npts):          # i = 0 .. n
        fdd[i, 0] = y[i]

    # Columnas siguientes: cada diferencia dividida se calcula a partir de
    # las dos adyacentes de la columna anterior.
    # Pseudocódigo: DOFOR j = 1, n ; DOFOR i = 0, n - j
    for j in range(1, npts):       # j = 1 .. n
        for i in range(npts - j):  # i = 0 .. n - j
            fdd[i, j] = (fdd[i + 1, j - 1] - fdd[i, j - 1]) / (x[i + j] - x[i])

    # ------------------------------------------------------------------
    # Evaluación del polinomio de Newton en xi, acumulando por orden.
    # ------------------------------------------------------------------
    yint = np.zeros(npts)          # estimaciones de orden 0 .. n
    ea = np.full(npts, np.nan)     # error aproximado por orden

    xterm = 1.0                    # producto (xi - x0)(xi - x1)...
    yint[0] = fdd[0, 0]            # estimación de orden 0

    # Pseudocódigo: DOFOR order = 1, n
    for order in range(1, npts):   # order = 1 .. n
        # El término se multiplica por (xi - x[order-1]).
        xterm = xterm * (xi - x[order - 1])
        # Nueva estimación = estimación previa + coef * término acumulado.
        yint2 = yint[order - 1] + fdd[0, order] * xterm
        # Error aproximado del orden anterior (diferencia entre estimaciones).
        ea[order - 1] = yint2 - yint[order - 1]
        yint[order] = yint2

    return yint, ea


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Ejemplo clásico de Chapra: estimar ln(2) por interpolación de Newton.
    # Se usan cuatro puntos (grado máximo 3) evaluando en xi = 2.
    # ------------------------------------------------------------------
    x = [1, 4, 6, 5]
    y = [0, 1.386294, 1.791759, 1.609438]
    xi = 2

    yint, ea = newt_int(x, y, xi)

    valor_real = np.log(2)  # ln(2) para comparar

    print(f"Interpolación de Newton en xi = {xi}")
    print(f"Valor real ln(2) = {valor_real:.6f}\n")

    # Encabezado de la tabla.
    print(f"{'Orden':>5} | {'Estimación yint':>16} | "
          f"{'Error aprox. (ea)':>18} | {'Error verdadero':>16}")
    print("-" * 66)

    for k in range(len(yint)):
        # Error verdadero relativo porcentual respecto a ln(2).
        et = abs((valor_real - yint[k]) / valor_real) * 100
        ea_str = f"{ea[k]:>18.7f}" if not np.isnan(ea[k]) else f"{'---':>18}"
        print(f"{k:>5} | {yint[k]:>16.6f} | {ea_str} | {et:>15.3f}%")

    print(f"\nResultado final (mayor orden): {yint[-1]:.6f}")

    # ------------------------------------------------------------------
    # Gráfica opcional: puntos de datos y polinomio interpolante.
    # ------------------------------------------------------------------
    try:
        import matplotlib.pyplot as plt

        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)

        # Malla fina para dibujar el polinomio; evaluamos newt_int en cada
        # punto y tomamos la estimación de mayor orden (yint[-1]).
        xs = np.linspace(x_arr.min(), x_arr.max(), 300)
        ys = np.array([newt_int(x_arr, y_arr, xv)[0][-1] for xv in xs])

        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, label="Polinomio de Newton (grado 3)", color="C0")
        plt.scatter(x_arr, y_arr, color="C3", zorder=5, label="Puntos de datos")
        plt.scatter([xi], [yint[-1]], color="C2", zorder=6,
                    label=f"Interpolación en xi={xi}")
        # Referencia: función real ln(x).
        plt.plot(xs, np.log(xs), "--", color="gray", label="ln(x) (real)")

        plt.title("Interpolación polinomial de Newton por diferencias divididas")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("\n(matplotlib no está instalado; se omite la gráfica.)")
