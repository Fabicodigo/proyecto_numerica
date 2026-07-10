"""
Regla del trapecio para integración numérica.

Implementación de los pseudocódigos de la Figura 21.9 de:
Chapra, S. C. y Canale, R. P. — "Métodos numéricos para ingenieros".

Se incluyen:
  a) trap(h, f0, f1)      -> regla del trapecio de un solo segmento.
  b) trapm(h, n, f)       -> regla del trapecio de múltiples segmentos.
  +  trapm_func(func,...) -> conveniencia para integrar una función dada.

La regla del trapecio aproxima la integral bajo la curva sustituyendo la
función por segmentos de recta entre nodos y sumando las áreas de los
trapecios resultantes.
"""

import numpy as np


def trap(h, f0, f1):
    """
    Regla del trapecio de un solo segmento.

    Reproduce la FUNCTION Trap de la Figura 21.9a de Chapra.

    Parámetros
    ----------
    h : float
        Ancho del segmento (b - a).
    f0 : float
        Valor de la función en el extremo izquierdo, f(a).
    f1 : float
        Valor de la función en el extremo derecho, f(b).

    Retorna
    -------
    float
        Área del trapecio = h * (f0 + f1) / 2.
    """
    # Área del trapecio: ancho por el promedio de las alturas.
    return h * (f0 + f1) / 2


def trapm(h, n, f):
    """
    Regla del trapecio de múltiples segmentos.

    Reproduce la FUNCTION Trapm de la Figura 21.9b de Chapra.

    Parámetros
    ----------
    h : float
        Ancho de cada segmento (todos iguales).
    n : int
        Número de segmentos (hay n+1 nodos: f[0] .. f[n]).
    f : array_like
        Valores de la función en los n+1 nodos.

    Retorna
    -------
    float
        Integral aproximada = h * (f0 + 2*Σ interiores + fn) / 2.

    Notas
    -----
    Los extremos f[0] y f[n] cuentan una vez; los nodos interiores
    (i = 1 .. n-1) cuentan doble, porque son compartidos por dos
    trapecios adyacentes.
    """
    f = np.asarray(f, dtype=float)

    # Se inicia la suma con el extremo izquierdo.
    # Pseudocódigo: sum = f0
    suma = f[0]

    # Nodos interiores: cada uno se suma multiplicado por 2.
    # Pseudocódigo: DOFOR i = 1, n-1  ->  range(1, n) en Python
    for i in range(1, n):          # i = 1 .. n-1
        suma = suma + 2 * f[i]

    # Se agrega el extremo derecho una sola vez.
    # Pseudocódigo: sum = sum + f[n]
    suma = suma + f[n]

    # Factor común h/2 de toda la fórmula compuesta.
    return h * suma / 2


def trapm_func(func, a, b, n):
    """
    Integra una función con la regla del trapecio de múltiples segmentos.

    Función de conveniencia: dada func, el intervalo [a, b] y el número de
    segmentos n, calcula el paso, genera los nodos y sus valores, y delega
    en trapm.

    Parámetros
    ----------
    func : callable
        Función a integrar; se evalúa como func(x).
    a, b : float
        Límites del intervalo de integración.
    n : int
        Número de segmentos.

    Retorna
    -------
    float
        Integral aproximada de func en [a, b].
    """
    # Ancho de cada segmento.
    h = (b - a) / n

    # Nodos equiespaciados: n+1 puntos de a hasta b.
    x = np.linspace(a, b, n + 1)

    # Valores de la función en cada nodo.
    f = func(x)

    # Se aplica la regla del trapecio de múltiples segmentos.
    return trapm(h, n, f)


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Ejemplo clásico de Chapra: integrar el polinomio de grado 5
    #   f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    # en el intervalo [0, 0.8]. Valor exacto de la integral = 1.640533.
    # ------------------------------------------------------------------
    def f(x):
        return (0.2 + 25 * x - 200 * x**2 + 675 * x**3
                - 900 * x**4 + 400 * x**5)

    a, b = 0.0, 0.8
    exacto = 1.640533

    print("Regla del trapecio")
    print(f"Integrando f(x) en [{a}, {b}]")
    print(f"Valor exacto = {exacto:.6f}\n")

    # --- Un solo segmento (trap) -------------------------------------
    h = b - a
    estimacion_1 = trap(h, f(a), f(b))
    et_1 = abs((exacto - estimacion_1) / exacto) * 100
    print(f"{'Método':<28}{'Estimación':>14}{'Error rel. %':>16}")
    print("-" * 58)
    print(f"{'1 segmento  (trap)':<28}{estimacion_1:>14.6f}{et_1:>15.3f}%")

    # --- Múltiples segmentos (trapm_func) ----------------------------
    for n in (2, 4):
        estimacion_n = trapm_func(f, a, b, n)
        et_n = abs((exacto - estimacion_n) / exacto) * 100
        etiqueta = f"{n} segmentos (trapm)"
        print(f"{etiqueta:<28}{estimacion_n:>14.6f}{et_n:>15.3f}%")

    # ------------------------------------------------------------------
    # Gráfica opcional: función real y aproximación por trapecios (n=4).
    # ------------------------------------------------------------------
    try:
        import matplotlib.pyplot as plt

        # Curva suave de la función real.
        xs = np.linspace(a, b, 300)
        ys = f(xs)

        # Nodos de la aproximación por trapecios con n = 4.
        n_graf = 4
        xn = np.linspace(a, b, n_graf + 1)
        fn = f(xn)

        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, color="C0", label="f(x) real")
        # Los segmentos de recta que unen los nodos forman los trapecios.
        plt.plot(xn, fn, "o-", color="C3",
                 label=f"Aproximación por trapecios (n={n_graf})")
        plt.fill_between(xn, fn, alpha=0.2, color="C3")

        plt.title("Regla del trapecio de múltiples segmentos")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("\n(matplotlib no está instalado; se omite la gráfica.)")
