import numpy as np
from core.stopping import criterio_parada
from core.plot_helper import inicializar_grafico, actualizar_grafico, finalizar_grafico
from core.ui import pedir_float

def secante(func, x0, x1, tol=1e-6, max_iter=150, plot_evolution=True, domain_grafico=None):
    """
    Método de la Secante para encontrar raíces de una función.
    
    Parámetros:
    - func: función f(x) a evaluar.
    - x0, x1: aproximaciones iniciales.
    - tol: tolerancia para el error relativo aproximado o |f(x)|.
    - max_iter: número máximo de iteraciones.
    - plot_evolution: boolean para activar/desactivar la evolución gráfica interactiva.
    - domain_grafico: tupla (xmin, xmax) para el dominio del gráfico. Si es None, se solicita al usuario.
    """
    # Si se requiere graficación y no hay dominio, se solicita al usuario
    if plot_evolution and domain_grafico is None:
        print("\nPara el método de la Secante se requiere definir el dominio del gráfico.")
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
                                     titulo=f"Secante: Evolución Gráfica (x0={x0}, x1={x1})")

    # Encabezado de la tabla de iteraciones
    print("\n" + "=" * 70)
    print(f"{'Iteración':^10} | {'Punto x':^16} | {'f(x)':^16} | {'Error Rel. Aprox.':^20}")
    print("-" * 70)
    
    y0 = func(x0)
    y1 = func(x1)
    
    iterations = []
    # Guardar los dos valores iniciales
    iterations.append({
        "iter": 0,
        "x": float(x0),
        "fx": float(y0),
        "error": None
    })
    iterations.append({
        "iter": 1,
        "x": float(x1),
        "fx": float(y1),
        "error": None
    })

    # Imprimir los estados iniciales
    print(f"{0:^10} | {x0:^16.8f} | {y0:^16.8e} | {'N/A':^20}")
    if plot_evolution:
        actualizar_grafico(fig, ax, 0, x0, y0)
        
    print(f"{1:^10} | {x1:^16.8f} | {y1:^16.8e} | {'N/A':^20}")
    if plot_evolution:
        actualizar_grafico(fig, ax, 1, x1, y1)
        
    raiz = None
    mensaje_fin = ""
    iteraciones_totales = 1
    
    # Verificar si alguna aproximación inicial ya es raíz
    stop, msg = criterio_parada(error=None, fx=y1, iteracion=1, tol=tol, max_iter=max_iter)
    if stop:
        raiz = x1
        mensaje_fin = msg
        
    if raiz is None:
        for i in range(2, max_iter + 1):
            iteraciones_totales = i
            denom = y1 - y0
            
            if abs(denom) < 1e-12:
                mensaje_fin = f"División por cero (o diferencia casi nula) detectada en el denominador en la iteración {i}."
                raiz = x1
                break
                
            x_new = x1 - y1 * (x1 - x0) / denom
            y_new = func(x_new)
            
            # Calcular error relativo aproximado
            if x_new != 0:
                ea = abs((x_new - x1) / x_new)
            else:
                ea = abs(x_new - x1)
                
            ea_str = f"{ea:.8e}"
                
            # Guardar iteración en la lista para la GUI
            iterations.append({
                "iter": i,
                "x": float(x_new),
                "fx": float(y_new),
                "error": float(ea)
            })

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
                
            # Desplazar variables
            x0, y0 = x1, y1
            x1, y1 = x_new, y_new
            
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
        "success": abs(func(raiz)) <= tol,
        "message": mensaje_fin,
        "root": raiz,
        "f_root": func(raiz),
        "iterations": iterations,

        "raiz": raiz,
        "f_raiz": func(raiz),
        "iteraciones": iteraciones_totales,
        "mensaje": mensaje_fin
    }