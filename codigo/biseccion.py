import numpy as np
from core.stopping import criterio_parada
from core.plot_helper import inicializar_grafico, actualizar_grafico, finalizar_grafico

def biseccion(func, a, b, tol=1e-6, max_iter=150, plot_evolution=True):
    """
    Método de Bisección para encontrar raíces de una función.
    
    Parámetros:
    - func: función f(x) a evaluar.
    - a, b: extremos del intervalo de búsqueda.
    - tol: tolerancia para el error relativo aproximado o |f(x)|.
    - max_iter: número máximo de iteraciones.
    - plot_evolution: boolean para activar/desactivar la evolución gráfica interactiva.
    """
    fa = func(a)
    fb = func(b)
    
    # Validar teorema de Bolzano
    if fa * fb > 0:
        raise ValueError(f"La función f(a)={fa:.4e} y f(b)={fb:.4e} deben tener signos opuestos en el intervalo [{a}, {b}].")
        
    # Encabezado de la tabla de iteraciones
    print("\n" + "=" * 70)
    print(f"{'Iteración':^10} | {'Punto x (m)':^16} | {'f(x)':^16} | {'Error Rel. Aprox.':^20}")
    print("-" * 70)
    
    fig, ax = None, None
    if plot_evolution:
        fig, ax = inicializar_grafico(func, a, b, titulo=f"Bisección: Evolución Gráfica en [{a}, {b}]")
        
    x_old = None
    raiz = None
    mensaje_fin = ""
    iteraciones_totales = 0
    iterations = []
    
    for i in range(1, max_iter + 1):
        iteraciones_totales = i
        x_new = (a + b) / 2.0
        y_new = func(x_new)
        
        # Calcular error relativo aproximado
        if x_old is not None:
            if x_new != 0:
                ea = abs((x_new - x_old) / x_new)
            else:
                ea = abs(x_new - x_old)
            ea_str = f"{ea:.8e}"
        else:
            ea = None
            ea_str = "N/A"
            
        # Guardar iteración en la lista para la GUI
        iterations.append({
            "iter": i,
            "x": float(x_new),
            "fx": float(y_new),
            "error": None if ea is None else float(ea)
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
            
        # Actualizar intervalo
        if fa * y_new < 0:
            b = x_new
            fb = y_new
        else:
            a = x_new
            fa = y_new
            
        x_old = x_new
        
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
        "success": mensaje_fin != "Se alcanzó el máximo de iteraciones",
        "message": mensaje_fin,
        "root": raiz,
        "f_root": func(raiz),
        "iterations": iterations,

        "raiz": raiz,
        "f_raiz": func(raiz),
        "iteraciones": iteraciones_totales,
        "mensaje": mensaje_fin
    }