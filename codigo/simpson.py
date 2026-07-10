"""
Reglas de Simpson para integración numérica.

Implementación de los pseudocódigos de la Figura 21.13 de:
Chapra, S. C. y Canale, R. P. — "Métodos numéricos para ingenieros".

Se incluyen:
  a) simp13(h, f0, f1, f2)          -> Simpson 1/3 simple  (3 puntos, 2 seg.)
  b) simp38(h, f0, f1, f2, f3)      -> Simpson 3/8 simple  (4 puntos, 3 seg.)
  c) simp13m(h, n, f)               -> Simpson 1/3 múltiple (n par)
  +  trap(h, f0, f1)                -> trapecio simple (usado si n = 1)
  d) simp_int(a, b, n, f)           -> función maestra que combina todo
  +  simp_int_func(func, a, b, n)   -> conveniencia para integrar una función

Las reglas de Simpson ajustan polinomios de grado 2 (1/3) o 3 (3/8) a los
nodos, en lugar de rectas como el trapecio, logrando mayor precisión.
"""

import numpy as np


def trap(h, f0, f1):
    """
    Regla del trapecio de un solo segmento (Figura 21.9a).

    Necesaria para el caso n = 1 dentro de simp_int.
    """
    return h * (f0 + f1) / 2


def simp13(h, f0, f1, f2):
    """
    Regla de Simpson 1/3 de una sola aplicación (Figura 21.13a).

    Usa 3 puntos igualmente espaciados (2 segmentos): f0, f1, f2.
    Ajusta una parábola a esos tres puntos.

    Parámetros
    ----------
    h : float
        Ancho de cada uno de los 2 segmentos.
    f0, f1, f2 : float
        Valores de la función en los 3 nodos.

    Retorna
    -------
    float
        Integral aproximada = 2h*(f0 + 4*f1 + f2)/6.
    """
    return 2 * h * (f0 + 4 * f1 + f2) / 6


def simp38(h, f0, f1, f2, f3):
    """
    Regla de Simpson 3/8 de una sola aplicación (Figura 21.13b).

    Usa 4 puntos igualmente espaciados (3 segmentos): f0, f1, f2, f3.
    Ajusta un polinomio cúbico a esos cuatro puntos.

    Parámetros
    ----------
    h : float
        Ancho de cada uno de los 3 segmentos.
    f0, f1, f2, f3 : float
        Valores de la función en los 4 nodos.

    Retorna
    -------
    float
        Integral aproximada = 3h*(f0 + 3*(f1+f2) + f3)/8.
    """
    return 3 * h * (f0 + 3 * (f1 + f2) + f3) / 8


def simp13m(h, n, f):
    """
    Regla de Simpson 1/3 de aplicación múltiple (Figura 21.13c).

    Requiere que 'n' (número de segmentos) sea PAR.

    Parámetros
    ----------
    h : float
        Ancho de cada segmento.
    n : int
        Número de segmentos (par). Usa los nodos f[0] .. f[n].
    f : array_like
        Valores de la función en los nodos (al menos n+1 elementos;
        solo se acceden los índices 0 .. n).

    Retorna
    -------
    float
        Integral aproximada = h*(f0 + 4*Σimpares + 2*Σpares + fn)/3.

    Notas
    -----
    Los nodos de índice impar pesan 4 y los pares interiores pesan 2,
    porque cada parábola cubre 2 segmentos y los puntos intermedios
    (impares) son los vértices de cada parábola.
    """
    f = np.asarray(f, dtype=float)

    # Se inicia con el extremo izquierdo.
    # Pseudocódigo: sum = f(0)
    suma = f[0]

    # Recorre los nodos de índice impar (vértices de cada parábola),
    # sumando 4*f[i] y 2*f[i+1] (el par que le sigue, interior).
    # Pseudocódigo: DOFOR i = 1, n-2, 2  ->  range(1, n-1, 2) en Python
    for i in range(1, n - 1, 2):   # i = 1, 3, 5, ..., n-3
        suma = suma + 4 * f[i] + 2 * f[i + 1]

    # Último nodo impar (peso 4) y extremo derecho (peso 1).
    # Pseudocódigo: sum = sum + 4*f[n-1] + f[n]
    suma = suma + 4 * f[n - 1] + f[n]

    # Factor común h/3.
    return h * suma / 3


def simp_int(a, b, n, f):
    """
    Función maestra de integración por reglas de Simpson (Figura 21.13d).

    Decide automáticamente qué combinación de reglas aplicar según n:
      - n = 1        -> regla del trapecio.
      - n par        -> Simpson 1/3 múltiple.
      - n impar > 1  -> Simpson 3/8 a los últimos 3 segmentos + Simpson 1/3
                        múltiple a los primeros m = n - 3 segmentos.

    Parámetros
    ----------
    a, b : float
        Límites del intervalo de integración.
    n : int
        Número de segmentos (hay n+1 nodos).
    f : array_like
        Valores de la función en los n+1 nodos, f[0] .. f[n].

    Retorna
    -------
    float
        Integral aproximada sobre [a, b].
    """
    f = np.asarray(f, dtype=float)

    # Ancho de cada segmento.
    h = (b - a) / n

    # Acumulador (el pseudocódigo asume sum = 0 al inicio).
    suma = 0.0

    if n == 1:
        # Un solo segmento: no alcanza para Simpson, se usa el trapecio.
        # Pseudocódigo: sum = Trap(h, f[n-1], f[n])  (aquí f[0], f[1])
        suma = trap(h, f[n - 1], f[n])
    else:
        m = n
        # ¿n es impar? El pseudocódigo lo detecta con odd = n/2 - INT(n/2).
        odd = (n % 2) == 1

        if odd and n > 1:
            # Se aplica Simpson 3/8 a los ÚLTIMOS 4 nodos (3 segmentos):
            # f[n-3], f[n-2], f[n-1], f[n].
            suma = suma + simp38(h, f[n - 3], f[n - 2], f[n - 1], f[n])
            # El resto son m = n - 3 segmentos (número par), para Simpson 1/3.
            m = n - 3

        if m > 1:
            # Simpson 1/3 múltiple sobre los PRIMEROS m segmentos.
            # simp13m solo accede a los índices 0..m del arreglo, que son
            # exactamente los primeros m+1 nodos, así que pasamos f completo.
            suma = suma + simp13m(h, m, f)

    return suma


def simp_int_func(func, a, b, n):
    """
    Integra una función con las reglas de Simpson (vía simp_int).

    Función de conveniencia: dada func, el intervalo [a, b] y el número de
    segmentos n, calcula el paso, genera los nodos y sus valores, y delega
    en simp_int.

    Parámetros
    ----------
    func : callable
        Función a integrar; se evalúa como func(x).
    a, b : float
        Límites del intervalo.
    n : int
        Número de segmentos.

    Retorna
    -------
    float
        Integral aproximada de func en [a, b].
    """
    # Nodos equiespaciados: n+1 puntos de a hasta b.
    x = np.linspace(a, b, n + 1)
    # Valores de la función en cada nodo.
    f = func(x)
    # Se delega en la función maestra.
    return simp_int(a, b, n, f)


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Ejemplo clásico de Chapra: integrar el polinomio de grado 5
    #   f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    # en [0, 0.8]. Valor exacto de la integral = 1.640533.
    # ------------------------------------------------------------------
    def f(x):
        return (0.2 + 25 * x - 200 * x**2 + 675 * x**3
                - 900 * x**4 + 400 * x**5)

    a, b = 0.0, 0.8
    exacto = 1.640533

    print("Reglas de Simpson")
    print(f"Integrando f(x) en [{a}, {b}]")
    print(f"Valor exacto = {exacto:.6f}\n")

    print(f"{'Método':<34}{'Estimación':>13}{'Error rel. %':>15}")
    print("-" * 62)

    # --- Simpson 1/3 simple, n = 2 (3 nodos) -------------------------
    h2 = (b - a) / 2
    x2 = np.linspace(a, b, 3)
    est_13 = simp13(h2, *f(x2))
    et_13 = abs((exacto - est_13) / exacto) * 100
    print(f"{'Simpson 1/3 simple (n=2)':<34}{est_13:>13.6f}{et_13:>14.4f}%")

    # --- Simpson 3/8 simple, n = 3 (4 nodos) -------------------------
    h3 = (b - a) / 3
    x3 = np.linspace(a, b, 4)
    est_38 = simp38(h3, *f(x3))
    et_38 = abs((exacto - est_38) / exacto) * 100
    print(f"{'Simpson 3/8 simple (n=3)':<34}{est_38:>13.6f}{et_38:>14.4f}%")

    # --- Función maestra con varios n --------------------------------
    for n in (4, 5, 6):
        est_n = simp_int_func(f, a, b, n)
        et_n = abs((exacto - est_n) / exacto) * 100
        # Etiqueta que indica qué combinación usa internamente.
        if n % 2 == 0:
            detalle = "1/3 múltiple"
        else:
            detalle = "3/8 + 1/3 múltiple"
        etiqueta = f"simp_int (n={n}, {detalle})"
        print(f"{etiqueta:<34}{est_n:>13.6f}{et_n:>14.4f}%")

    # ------------------------------------------------------------------
    # Gráfica opcional: función real y nodos usados (n=6).
    # ------------------------------------------------------------------
    try:
        import matplotlib.pyplot as plt

        xs = np.linspace(a, b, 300)
        ys = f(xs)

        n_graf = 6
        xn = np.linspace(a, b, n_graf + 1)
        fn = f(xn)

        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, color="C0", label="f(x) real")
        plt.fill_between(xs, ys, alpha=0.15, color="C0")
        plt.scatter(xn, fn, color="C3", zorder=5,
                    label=f"Nodos usados (n={n_graf})")

        plt.title("Reglas de Simpson (integración numérica)")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("\n(matplotlib no está instalado; se omite la gráfica.)")
