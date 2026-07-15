from config import APP_TITLE, APP_VERSION, DEFAULT_TOL, DEFAULT_MAX_ITER
from core.ui import (
    titulo_principal,
    subtitulo,
    mensaje_info,
    mensaje_ok,
    mensaje_error,
    pausa,
    pedir_opcion,
    pedir_float,
    pedir_float_positivo,
    pedir_int_positivo,
    pedir_lista_floats,
    pedir_puntos_xy,
    pedir_funcion_texto,
    pedir_intervalo,
    pedir_matriz_vector,
    pedir_vector_inicial,
    mostrar_resultado_escalar,
    mostrar_resultado_texto,
    mostrar_resultado_newton_interpolacion,
    mostrar_matriz
)
from core.parser import construir_funcion

from codigo.biseccion import biseccion
from codigo.newton_raices import newton
from codigo.secante import secante
from codigo.ejercicios import menu_ejercicios_predefinidos
from codigo.problemas_seccion_18 import menu_guia_18
from codigo.gauss_pivoteo import gauss_pivoteo_parcial
from codigo.gauss_seidel import gauss_seidel
from codigo.newton_interpolacion import newt_int
from codigo.lagrange_interpolacion import lagrange
from codigo.trapecio import trapm_func
from codigo.simpson import simp_int_func

def menu_principal():
    while True:
        titulo_principal(f"{APP_TITLE} {APP_VERSION}")
        print("1. Métodos de raíces")
        print("2. Sistemas de ecuaciones lineales")
        print("3. Interpolación")
        print("4. Integración numérica")
        print("0. Salir")

        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "3", "4", "0"])

        if opcion == "1":
            menu_raices()
        elif opcion == "2":
            menu_sistemas()
        elif opcion == "3":
            menu_interpolacion()
        elif opcion == "4":
            menu_integracion()
        elif opcion == "0":
            mensaje_ok("Saliendo del programa...")
            break

def menu_raices():
    while True:
        titulo_principal("MÓDULO DE RAÍCES DE FUNCIONES")
        print("1. Bisección (Manual)")
        print("2. Newton (Manual)")
        print("3. Secante (Manual)")
        print("4. Resolver Ejercicios Propuestos (Ej 6, Ej 7, Abrevadero)")
        print("0. Volver")

        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "3", "4", "0"])

        if opcion == "1":
            try:
                expr = pedir_funcion_texto()
                func = construir_funcion(expr)
                a, b = pedir_intervalo()
                tol = pedir_float_positivo("Ingrese la tolerancia: ")
                resultado = biseccion(func, a, b, tol=tol, max_iter=DEFAULT_MAX_ITER)
                mostrar_resultado_texto("RESULTADOS - BISECCIÓN", str(resultado))
            except Exception as e:
                mensaje_error(f"Error al ejecutar Bisección: {e}")
            pausa()

        elif opcion == "2":
            try:
                expr = pedir_funcion_texto()
                func = construir_funcion(expr)
                dexpr = input("Ingrese la derivada f'(x): ").strip()
                dfunc = construir_funcion(dexpr)
                x0 = pedir_float("Ingrese la aproximación inicial x0: ")
                tol = pedir_float_positivo("Ingrese la tolerancia: ")
                resultado = newton(func, dfunc, x0, tol=tol, max_iter=DEFAULT_MAX_ITER)
                mostrar_resultado_texto("RESULTADOS - NEWTON", str(resultado))
            except Exception as e:
                mensaje_error(f"Error al ejecutar Newton: {e}")
            pausa()

        elif opcion == "3":
            try:
                expr = pedir_funcion_texto()
                func = construir_funcion(expr)
                x0 = pedir_float("Ingrese x0: ")
                x1 = pedir_float("Ingrese x1: ")
                tol = pedir_float_positivo("Ingrese la tolerancia: ")
                resultado = secante(func, x0, x1, tol=tol, max_iter=DEFAULT_MAX_ITER)
                mostrar_resultado_texto("RESULTADOS - SECANTE", str(resultado))
            except Exception as e:
                mensaje_error(f"Error al ejecutar Secante: {e}")
            pausa()

        elif opcion == "4":
            menu_ejercicios_predefinidos()

        elif opcion == "0":
            break

def menu_sistemas():
    while True:
        titulo_principal("MÓDULO DE SISTEMAS DE ECUACIONES")
        print("1. Gauss con pivoteo parcial")
        print("2. Gauss-Seidel")
        print("0. Volver")

        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "0"])

        if opcion == "1":
            try:
                A, b = pedir_matriz_vector()
                mostrar_matriz(A, "Matriz A")
                mostrar_resultado_texto("Vector b", str(b))
                resultado = gauss_pivoteo_parcial(A, b)
                mostrar_resultado_texto("RESULTADOS - GAUSS CON PIVOTEO", str(resultado))
            except NotImplementedError as e:
                mensaje_info(f"Método pendiente de integración: {e}")
            except Exception as e:
                mensaje_error(f"Error al ejecutar Gauss con pivoteo: {e}")
            pausa()

        elif opcion == "2":
            try:
                A, b = pedir_matriz_vector()
                usar_x0 = input("¿Desea ingresar un vector inicial? (s/n): ").strip().lower()

                if usar_x0 == "s":
                    x0 = pedir_vector_inicial(len(A))
                else:
                    x0 = None

                tol = pedir_float_positivo("Ingrese la tolerancia: ")
                resultado = gauss_seidel(A, b, x0=x0, tol=tol, max_iter=DEFAULT_MAX_ITER)
                mostrar_resultado_texto("RESULTADOS - GAUSS-SEIDEL", str(resultado))
            except NotImplementedError as e:
                mensaje_info(f"Método pendiente de integración: {e}")
            except Exception as e:
                mensaje_error(f"Error al ejecutar Gauss-Seidel: {e}")
            pausa()

        elif opcion == "0":
            break

def menu_interpolacion():
    while True:
        titulo_principal("MÓDULO DE INTERPOLACIÓN")
        print("1. Newton")
        print("2. Lagrange")
        print("3. Resolver Guía de Problemas 18 (18.5, 18.7, 18.8)")
        print("0. Volver")

        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "3", "0"])

        if opcion == "1":
            x, y = pedir_puntos_xy()
            if x is None:
                pausa()
                continue

            xi = pedir_float("Ingrese el valor xi a interpolar: ")

            try:
                yint, ea = newt_int(x, y, xi)
                mostrar_resultado_newton_interpolacion(xi, yint, ea)
            except Exception as e:
                mensaje_error(f"Error al ejecutar Newton: {e}")

            pausa()

        elif opcion == "2":
            x, y = pedir_puntos_xy()
            if x is None:
                pausa()
                continue

            xi = pedir_float("Ingrese el valor xi a interpolar: ")

            try:
                resultado = lagrange(x, y, xi)
                mostrar_resultado_escalar("RESULTADOS - INTERPOLACIÓN DE LAGRANGE", resultado)
            except Exception as e:
                mensaje_error(f"Error al ejecutar Lagrange: {e}")

            pausa()

        elif opcion == "3":
            menu_guia_18()

        elif opcion == "0":
            break

def menu_integracion():
    while True:
        titulo_principal("MÓDULO DE INTEGRACIÓN NUMÉRICA")
        print("1. Trapecio")
        print("2. Simpson")
        print("0. Volver")

        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "0"])

        if opcion == "1":
            try:
                expr = pedir_funcion_texto()
                func = construir_funcion(expr)
                a = pedir_float("Ingrese el extremo inferior a: ")
                b = pedir_float("Ingrese el extremo superior b: ")
                n = pedir_int_positivo("Ingrese el número de segmentos n: ")

                resultado = trapm_func(func, a, b, n)
                mostrar_resultado_escalar("RESULTADOS - REGLA DEL TRAPECIO", resultado)

            except Exception as e:
                mensaje_error(f"Error al ejecutar Trapecio: {e}")

            pausa()

        elif opcion == "2":
            try:
                mensaje_info("Use una función en x. Ejemplo: x**2, x**3, sin(x), exp(x)")
                expr = pedir_funcion_texto()
                func = construir_funcion(expr)
                a = pedir_float("Ingrese el extremo inferior a: ")
                b = pedir_float("Ingrese el extremo superior b: ")
                n = pedir_int_positivo("Ingrese el número de segmentos n: ")

                resultado = simp_int_func(func, a, b, n)
                mostrar_resultado_escalar("RESULTADOS - REGLA DE SIMPSON", resultado)

            except Exception as e:
                mensaje_error(f"Error al ejecutar Simpson: {e}")

            pausa()

        elif opcion == "0":
            break

if __name__ == "__main__":
    menu_principal()