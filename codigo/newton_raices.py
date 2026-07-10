import numpy as np
from core.stopping import criterio_parada
from core.plot_helper import inicializar_grafico, actualizar_grafico, finalizar_grafico
from core.ui import pedir_float

def newton(func, dfunc, x0, tol=1e-6, max_iter=150, plot_evolution=True, domain_grafico=None):
    """
    Método de Newton-Raphson para encontrar raíces de una función.
    
    Parámetros:
    - func: función f(x) a evaluar.
    - dfunc: derivada de la función f'(x).
    - x0: aproximación inicial.
    - tol: tolerancia para el error relativo aproximado o |f(x)|.
    - max_iter: número máximo de iteraciones.
    - plot_evolution: boolean para activar/desactivar la evolución gráfica interactiva.
    - domain_grafico: tupla (xmin, xmax) para el dominio del gráfico. Si es None, se solicita al usuario.
    """
    # Si se requiere graficación y no hay dominio, se solicita al usuario
    if plot_evolution and domain_grafico is None:
        print("\nPara el método de Newton se requiere definir el dominio del gráfico.")
        while True:
            xmin = pedir_float("Ingrese el límite inferior del dominio (xmin): ")
            xmax = pedir_float("Ingrese el límite superior del dominio (xmax): ")
            if xmin < xmax:
                domain_grafico = (xmin, xmax)
                break
            print("[ERROR] El límite inferior xmin debe ser menor que el límite superior xmax.")
            
    # Inicializar graficación
    fig, ax = None, None
    if plot_evolution:
        fig, ax = inicializar_grafico(func, domain_grafico[0], domain_grafico[1], 
                                     titulo=f"Newton-Raphson: Evolución Gráfica (x0={x0})")

    # Encabezado de la tabla de iteraciones
    print("\n" + "=" * 70)
    print(f"{'Iteración':^10} | {'Punto x':^16} | {'f(x)':^16} | {'Error Rel. Aprox.':^20}")
    print("-" * 70)
    
    x_old = x0
    y_old = func(x_old)
    
    # Imprimir el estado inicial (Iteración 0)
    print(f"{0:^10} | {x_old:^16.8f} | {y_old:^16.8e} | {'N/A':^20}")
    if plot_evolution:
        actualizar_grafico(fig, ax, 0, x_old, y_old)
        
    raiz = None
    mensaje_fin = ""
    iteraciones_totales = 0
    
    # Evaluar si la aproximación inicial ya es raíz
    stop, msg = criterio_parada(error=None, fx=y_old, iteracion=0, tol=tol, max_iter=max_iter)
    if stop:
        raiz = x0
        mensaje_fin = msg
        
    if raiz is None:
        for i in range(1, max_iter + 1):
            iteraciones_totales = i
            dfx = dfunc(x_old)
            
            if abs(dfx) < 1e-12:
                mensaje_fin = f"Derivada casi nula detectada (f'(x) = {dfx:.4e}) en x = {x_old:.8f}"
                raiz = x_old
                break
                
            x_new = x_old - y_old / dfx
            y_new = func(x_new)
            
            # Calcular error relativo aproximado
            if x_new != 0:
                ea = abs((x_new - x_old) / x_new)
            else:
                ea = abs(x_new - x_old)
                
            ea_str = f"{ea:.8e}"
                
            # Imprimir fila de la tabla
            print(f"{i:^10} | {x_new:^16.8f} | {y_new:^16.8e} | {ea_str:^20}")
            
            # Graficar iterado en vivo
            if plot_evolution:
                actualizar_grafico(fig, ax, i, x_new, y_new)
                
            # Criterio de parada
            stop, msg = criterio_parada(error=ea, fx=y_new, iteracion=i, tol=tol, max_iter=max_iter)
            if stop:
                raiz = x_new
                mensaje_fin = msg
                break
                
            x_old = x_new
            y_old = y_new
            
    if raiz is None:
        raiz = x_new
        mensaje_fin = "Se alcanzó el máximo de iteraciones"
        
    print("=" * 70)
    
    # Mostrar resultados en pantalla
    print(f"Criterio de parada cumplido: {mensaje_fin}")
    print(f"Valor al que converge: {raiz:.10f}")
    print(f"Evaluación de la función f(x) en el valor obtenido: {func(raiz):.10e}")
    print("=" * 70 + "\n")
    
    if plot_evolution:
        finalizar_grafico(fig, ax, raiz, func(raiz), f"Raíz: {raiz:.6f}\n{mensaje_fin}")
        
    return {
        "raiz": raiz,
        "f_raiz": func(raiz),
        "iteraciones": iteraciones_totales,
        "mensaje": mensaje_fin
    }