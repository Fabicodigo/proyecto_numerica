"""
Guía de problemas — Chapra, Capítulo 18 (Interpolación).

Resolución con código de los problemas 18.5, 18.6 y 18.7 de
Chapra & Canale, "Métodos numéricos para ingenieros".

No se reescribe ningún método: se reutilizan las implementaciones
del proyecto (newt_int, lagrange y biseccion) y solo se orquestan
para cada problema.
"""

import numpy as np
from core.ui import titulo_principal, subtitulo, mensaje_info, mensaje_ok, pausa, pedir_opcion
from codigo.newton_interpolacion import newt_int
from codigo.lagrange_interpolacion import lagrange
from codigo.biseccion import biseccion

# ----------------------------------------------------------------------
# Datos de la tabla (problemas 18.5 y 18.6). Provienen exactamente del
# polinomio f(x) = x^3 - x^2 - x + 4, por lo que el valor verdadero de
# la interpolación en x = 4 es f(4) = 48.
# ----------------------------------------------------------------------
XI = 4.0
VALOR_REAL = XI**3 - XI**2 - XI + 4


def run_problema_18_5():
    """
    Problema 18.5 — Interpolación de Newton (órdenes 1 a 4).

    Los puntos base se pasan ordenados por cercanía a xi = 4 para que
    cada orden k use los k+1 puntos más próximos: {3, 5, 2, 7, 1}.
    Una sola llamada a newt_int entrega la estimación de cada orden y
    su error aproximado.
    """
    subtitulo("PROBLEMA 18.5 - INTERPOLACION DE NEWTON (ordenes 1 a 4)")

    x = [3, 5, 2, 7, 1]
    y = [19, 99, 6, 291, 3]

    print(f"\nDatos: x = [1, 2, 3, 5, 7, 8], f(x) = [3, 6, 19, 99, 291, 444]")
    print(f"Se estima f({XI:g}) con los puntos ordenados por cercanía a {XI:g}:")
    print(f"  x = {x}")
    print(f"  y = {y}")

    yint, ea = newt_int(x, y, XI)

    print(f"\n{'Orden':>5} | {'Estimación f(4)':>16} | {'Error aprox. (ea)':>18}")
    print("-" * 46)
    for k in range(1, len(yint)):
        ea_str = f"{ea[k]:>18.6f}" if not np.isnan(ea[k]) else f"{'---':>18}"
        print(f"{k:>5} | {yint[k]:>16.6f} | {ea_str}")

    print(f"\nValor verdadero f(4) = {VALOR_REAL:g} (los datos son x^3 - x^2 - x + 4).")
    print("El error se anula a partir del orden 3 (b4 = 0): un cúbico basta.")

    return yint


def run_problema_18_6():
    """
    Problema 18.6 — Interpolación de Lagrange (órdenes 1 a 3).

    A diferencia de Newton, lagrange entrega una sola estimación por
    conjunto de nodos, así que se hace una llamada por orden con los
    nodos más cercanos a xi = 4. Se compara con Newton (18.5).
    """
    subtitulo("PROBLEMA 18.6 - INTERPOLACION DE LAGRANGE (ordenes 1 a 3)")

    casos = {
        1: ([3, 5], [19, 99]),
        2: ([2, 3, 5], [6, 19, 99]),
        3: ([2, 3, 5, 7], [6, 19, 99, 291]),
    }

    resultados = {}
    print(f"\n{'Orden':>5} | {'Nodos':>14} | {'Estimación f(4)':>16}")
    print("-" * 43)
    for orden, (xn, yn) in casos.items():
        resultados[orden] = lagrange(xn, yn, XI)
        print(f"{orden:>5} | {str(xn):>14} | {resultados[orden]:>16.6f}")

    # Comparación con Newton: el polinomio interpolante es único, por lo
    # que ambos métodos deben dar exactamente lo mismo.
    yint, _ = newt_int([3, 5, 2, 7, 1], [19, 99, 6, 291, 3], XI)

    print("\n" + "=" * 40)
    print("COMPARACIÓN NEWTON (18.5) vs LAGRANGE (18.6)")
    print("=" * 40)
    print(f"{'Orden':>5} | {'Newton':>10} | {'Lagrange':>10}")
    print("-" * 33)
    for orden in (1, 2, 3):
        print(f"{orden:>5} | {yint[orden]:>10.6f} | {resultados[orden]:>10.6f}")

    print("\nSon idénticos: el polinomio interpolante de grado n por un")
    print("conjunto de puntos es único; Newton y Lagrange son dos formas")
    print("de escribir el mismo polinomio.")

    return resultados


def run_problema_18_7(plot_evolution=False):
    """
    Problema 18.7 — Interpolación inversa (cúbica + bisección).

    Dada la tabla de f(x) = 1/x, se busca el x tal que f(x) = 0.23.
    Se construye el polinomio cúbico de Newton con los 4 puntos más
    cercanos {3, 4, 5, 6} y se resuelve g(x) = p(x) - 0.23 = 0 con el
    método de bisección del proyecto en [4, 5] (hay cambio de signo).
    """
    subtitulo("PROBLEMA 18.7 - INTERPOLACION INVERSA (cubica + biseccion)")

    # Tabla de f(x) = 1/x (se corrige el error de transcripción del
    # enunciado: f(7) = 0.1429, no 1.1429).
    x4 = [3, 4, 5, 6]
    y4 = [0.3333, 0.25, 0.2, 0.1667]
    objetivo = 0.23

    # p(x): cúbico de Newton evaluado con newt_int (estimación de mayor
    # orden). g(x) = p(x) - 0.23: su raíz es el x buscado.
    def p(x):
        return newt_int(x4, y4, x)[0][-1]

    def g(x):
        return p(x) - objetivo

    print(f"\nDatos: x = [2..7], f(x) = 1/x. Se busca x tal que f(x) = {objetivo}.")
    print(f"Como f(4) = 0.25 > {objetivo} > 0.2 = f(5), la raíz está en [4, 5].")
    print(f"Cúbico de Newton con los 4 puntos más cercanos: x = {x4}, f = {y4}")
    print(f"Se resuelve g(x) = p(x) - {objetivo} = 0 por bisección "
          f"(g(4) = {g(4.0):+.4f}, g(5) = {g(5.0):+.4f}):")

    resultado = biseccion(g, 4.0, 5.0, tol=1e-5, plot_evolution=plot_evolution)

    x_real = 1 / objetivo  # los datos son f(x) = 1/x
    raiz = resultado["raiz"]

    print("=" * 70)
    print("RESULTADOS FINALES - PROBLEMA 18.7")
    print("=" * 70)
    print(f"x tal que f(x) = {objetivo}:      x = {raiz:.6f}")
    print(f"Verificación con el cúbico:   p({raiz:.6f}) = {p(raiz):.6f}")
    print(f"Valor real (1/{objetivo}):         x = {x_real:.6f}")
    print(f"Diferencia: {abs(raiz - x_real):.6f} (redondeo de la tabla + el cúbico")
    print("aproxima a 1/x). La interpolación inversa convierte un problema")
    print("sin despeje de x en uno de raíces: se combinan dos métodos.")
    print("=" * 70 + "\n")

    return resultado


def menu_guia_18():
    while True:
        titulo_principal("GUÍA DE PROBLEMAS 18 - CHAPRA (INTERPOLACIÓN)")
        print("1. Problema 18.5 (Newton, órdenes 1 a 4)")
        print("2. Problema 18.6 (Lagrange, órdenes 1 a 3 + comparación)")
        print("3. Problema 18.7 (Interpolación inversa: cúbica + bisección)")
        print("4. Ejecutar TODOS los problemas de una vez")
        print("0. Volver")

        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "3", "4", "0"])

        if opcion == "0":
            break

        # La graficación interactiva solo aplica al 18.7 (bisección).
        plot_evolution = False
        if opcion in ("3", "4"):
            graf_opc = pedir_opcion("¿Desea activar la graficación interactiva paso a paso? (s/n): ", ["s", "n"])
            plot_evolution = (graf_opc == "s")

        if opcion == "1":
            try:
                run_problema_18_5()
            except Exception as e:
                print(f"[ERROR] Ocurrió un error en el Problema 18.5: {e}")
            pausa()

        elif opcion == "2":
            try:
                run_problema_18_6()
            except Exception as e:
                print(f"[ERROR] Ocurrió un error en el Problema 18.6: {e}")
            pausa()

        elif opcion == "3":
            try:
                run_problema_18_7(plot_evolution=plot_evolution)
            except Exception as e:
                print(f"[ERROR] Ocurrió un error en el Problema 18.7: {e}")
            pausa()

        elif opcion == "4":
            try:
                mensaje_info("Ejecutando Problema 18.5...")
                run_problema_18_5()
                mensaje_info("Ejecutando Problema 18.6...")
                run_problema_18_6()
                mensaje_info("Ejecutando Problema 18.7...")
                run_problema_18_7(plot_evolution=plot_evolution)
                mensaje_ok("Todos los problemas de la guía 18 completados.")
            except Exception as e:
                print(f"[ERROR] Ocurrió un error general: {e}")
            pausa()
