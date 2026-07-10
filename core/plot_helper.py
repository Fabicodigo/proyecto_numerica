import matplotlib.pyplot as plt
import numpy as np

def inicializar_grafico(func, x_min, x_max, titulo="Evolución Gráfica del Método"):
    """
    Inicializa la figura de Matplotlib para la evolución en tiempo real.
    """
    # Habilitar modo interactivo
    plt.ion()
    fig, ax = plt.subplots(figsize=(9, 6))
    
    # Configurar estilo visual premium
    ax.set_facecolor('#F8FAFC')  # Fondo claro muy suave
    fig.patch.set_facecolor('#FFFFFF')
    ax.grid(True, linestyle='--', color='#E2E8F0', linewidth=0.8)
    
    # Eliminar bordes superior y derecho para diseño moderno
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')
    ax.tick_params(colors='#64748B')
    
    # Generar puntos de la curva
    # Si la función es discontinua o da errores en ciertos puntos, manejamos excepciones
    x_vals = np.linspace(x_min, x_max, 500)
    try:
        y_vals = func(x_vals)
    except Exception:
        # Si falla evaluar como vector, evaluar uno por uno
        y_vals = []
        for val in x_vals:
            try:
                y_vals.append(func(val))
            except Exception:
                y_vals.append(np.nan)
        y_vals = np.array(y_vals)
        
    # Graficar la curva principal
    ax.plot(x_vals, y_vals, '-', color='#6366F1', linewidth=2.5, label='f(x)')
    
    # Eje horizontal y = 0
    ax.axhline(0, color='#94A3B8', linestyle='-', linewidth=1.0, alpha=0.7)
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', color='#1E293B', pad=15)
    ax.set_xlabel("x", fontsize=11, color='#475569')
    ax.set_ylabel("f(x)", fontsize=11, color='#475569')
    
    plt.tight_layout()
    return fig, ax

def actualizar_grafico(fig, ax, iteracion, x, y, delay=0.3):
    """
    Dibuja un iterado en el gráfico en tiempo real con una breve pausa.
    """
    # Dibujar punto intermedio
    ax.plot(x, y, 'o', color='#EF4444', markersize=6, alpha=0.8)
    
    # Línea vertical punteada al eje X
    ax.vlines(x, 0, y, colors='#FDA4AF', linestyles='dotted', linewidth=1.2)
    
    # Etiqueta pequeña indicando el número de iteración
    ax.text(x, y, f"x{iteracion}", fontsize=8, color='#9F1239', 
            verticalalignment='bottom', horizontalalignment='right')
    
    # Actualizar la visualización de la ventana
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(delay)

def finalizar_grafico(fig, ax, x_root, y_root, mensaje=""):
    """
    Destaca el iterado final (la raíz) y desactiva el modo interactivo.
    """
    # Graficar la raíz obtenida con un marcador estrella dorada muy llamativo
    ax.plot(x_root, y_root, '*', color='#F59E0B', markersize=14, 
            markeredgecolor='#78350F', markeredgewidth=1.5, label=f'Raíz: {x_root:.6f}')
    
    # Mostrar mensaje del estado de convergencia
    if mensaje:
        ax.text(0.05, 0.95, mensaje, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
                                                   facecolor='#F1F5F9', edgecolor='#CBD5E1', alpha=0.9))
    
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0')
    
    # Desactivar interactividad para que la ventana permanezca abierta
    plt.ioff()
    fig.canvas.draw()
    plt.show()
