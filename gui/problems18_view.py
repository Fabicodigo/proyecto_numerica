import customtkinter as ctk
import numpy as np
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from codigo.newton_interpolacion import newt_int
from codigo.lagrange_interpolacion import lagrange
from codigo.biseccion import biseccion


# ----------------------------------------------------------------------
# Datos de los enunciados (Chapra, cap. 18). La tabla de 18.5/18.7
# proviene del polinomio f(x) = x^3 - x^2 - x + 4, por lo que el valor
# verdadero en x = 4 es f(4) = 48.
# ----------------------------------------------------------------------
X_DATOS = [1, 2, 3, 5, 7, 8]
Y_DATOS = [3, 6, 19, 99, 291, 444]
X_ORDENADOS = [3, 5, 2, 7, 1]
Y_ORDENADOS = [19, 99, 6, 291, 3]
XI = 4.0
VALOR_REAL = XI**3 - XI**2 - XI + 4

# Problema 18.8: tabla de f(x) = 1/x (se corrige el error de
# transcripción del enunciado: f(7) = 0.1429, no 1.1429).
X_INVERSA = [2, 3, 4, 5, 6, 7]
Y_INVERSA = [0.5, 0.3333, 0.25, 0.2, 0.1667, 0.1429]
X_NODOS_INV = [3, 4, 5, 6]
Y_NODOS_INV = [0.3333, 0.25, 0.2, 0.1667]
OBJETIVO = 0.23

P185 = "Problema 18.5 (Newton)"
P186 = "Problema 18.7 (Lagrange)"
P187 = "Problema 18.8 (Interp. inversa)"

SEP = "-" * 34

ENUNCIADOS = {
    P185: "\n".join([
        "ENUNCIADO (Chapra 18.5)",
        SEP,
        "Dados los datos:",
        "",
        f"  x    = {X_DATOS}",
        f"  f(x) = {Y_DATOS}",
        "",
        "calcule f(4) con polinomios de",
        "interpolación de Newton de órdenes",
        "1 a 4. Elija los puntos base para",
        "obtener una buena exactitud.",
        "¿Qué indican los resultados acerca",
        "del orden del polinomio que generó",
        "los datos?",
        "",
        "CÓMO SE RESUELVE",
        SEP,
        "1. Los puntos base se ordenan por",
        "   cercanía a xi = 4, de modo que",
        "   cada orden k use los k+1 puntos",
        "   más próximos:",
        "",
        "     x = {3, 5, 2, 7, 1}",
        "",
        "2. Una sola llamada a newt_int",
        "   (diferencias divididas) entrega",
        "   la estimación de cada orden y su",
        "   error aproximado:",
        "",
        "     ea[k] = yint[k+1] - yint[k]",
    ]),
    P186: "\n".join([
        "ENUNCIADO (Chapra 18.7)",
        SEP,
        "Repita el problema 18.5 con el",
        "empleo de polinomios de Lagrange",
        "de órdenes 1 a 3.",
        "",
        "CÓMO SE RESUELVE",
        SEP,
        "1. A diferencia de Newton, lagrange",
        "   entrega una sola estimación por",
        "   conjunto de nodos: se hace una",
        "   llamada por orden con los nodos",
        "   más cercanos a xi = 4:",
        "",
        "     Orden 1: {3, 5}",
        "     Orden 2: {2, 3, 5}",
        "     Orden 3: {2, 3, 5, 7}",
        "",
        "2. Se compara con Newton (18.5):",
        "   deben coincidir, porque el",
        "   polinomio interpolante que pasa",
        "   por un conjunto de puntos es",
        "   único.",
    ]),
    P187: "\n".join([
        "ENUNCIADO (Chapra 18.8)",
        SEP,
        "Emplee interpolación inversa, con",
        "un polinomio de interpolación",
        "cúbico y el método de bisección,",
        "para determinar el valor de x que",
        f"corresponde a f(x) = {OBJETIVO}, para",
        "los datos tabulados (f(x) = 1/x):",
        "",
        f"  x    = {X_INVERSA}",
        f"  f(x) = {Y_INVERSA}",
        "",
        "CÓMO SE RESUELVE",
        SEP,
        "1. Se construye el cúbico de Newton",
        "   p(x) con los 4 puntos más",
        f"   cercanos: x = {X_NODOS_INV}.",
        "",
        f"2. Como f(4) = 0.25 > {OBJETIVO} y",
        f"   f(5) = 0.2 < {OBJETIVO}, la solución",
        "   está en [4, 5] (cambio de signo).",
        "",
        f"3. Se resuelve g(x) = p(x) - {OBJETIVO} = 0",
        "   con bisección (tol = 1e-5).",
        "",
        "La interpolación inversa convierte",
        "un problema sin despeje de x en un",
        "problema de raíces: se combinan",
        "dos métodos.",
    ]),
}


class Problems18View(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1, minsize=420)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(4, weight=1)
        self.left_panel.grid_rowconfigure(7, weight=1)

        # Panel derecho
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(3, weight=1)

        # ===== IZQUIERDA =====
        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="Guía de Problemas — Cap. 18",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Contenedor para la opción del problema
        self.inputs_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.inputs_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.inputs_frame.grid_columnconfigure(0, weight=1)
        self.inputs_frame.grid_columnconfigure(1, weight=1)

        self.problem_label = ctk.CTkLabel(self.inputs_frame, text="Problema:")
        self.problem_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        self.problem_option = ctk.CTkOptionMenu(
            self.inputs_frame,
            values=[P185, P186, P187],
            command=self.update_enunciado
        )
        self.problem_option.grid(row=1, column=0, padx=10, pady=2, sticky="ew")

        self.enunciado_label = ctk.CTkLabel(self.left_panel, text="Enunciado y explicación:")
        self.enunciado_label.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="w")

        self.enunciado_box = ctk.CTkTextbox(
            self.left_panel, height=120, wrap="word",
            font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.enunciado_box.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.enunciado_box.configure(state="disabled")

        self.buttons_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.buttons_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.solve_button = ctk.CTkButton(
            self.buttons_frame,
            text="Resolver",
            command=self.solve
        )
        self.solve_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Limpiar",
            fg_color="gray40",
            hover_color="gray30",
            command=self.clear_fields
        )
        self.clear_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.result_label = ctk.CTkLabel(self.left_panel, text="Resultados e interpretación:")
        self.result_label.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")

        self.result_box = ctk.CTkTextbox(
            self.left_panel, height=180, wrap="word",
            font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.result_box.grid(row=7, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.result_box.insert("1.0", "Presione 'Resolver' para ejecutar el problema seleccionado.\n")
        self.result_box.configure(state="disabled")

        # ===== DERECHA =====
        self.graph_title = ctk.CTkLabel(
            self.right_panel,
            text="Gráfica del Problema",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.graph_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.reset_plot()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.canvas.draw()

        self.table_title = ctk.CTkLabel(
            self.right_panel,
            text="Tabla de Resultados",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.table_title.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="w")

        table_frame = ctk.CTkFrame(self.right_panel)
        table_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, show="headings", height=8)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar.set, xscroll=xscrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar.grid(row=1, column=0, sticky="ew")

        self.update_enunciado(P185)

    # ------------------------------------------------------------------
    # Utilidades de la vista
    # ------------------------------------------------------------------
    def write_box(self, box, text):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.configure(state="disabled")

    def update_enunciado(self, problem):
        self.write_box(self.enunciado_box, ENUNCIADOS[problem])

    def reset_plot(self):
        self.ax.clear()
        self.ax.set_title("Seleccione un problema y presione 'Resolver'")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)

    def clear_table(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()

    def setup_table(self, columns, rows):
        """columns: lista de (id, encabezado, ancho); rows: lista de tuplas."""
        self.clear_table()
        self.tree["columns"] = [c[0] for c in columns]
        for col_id, heading, width in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor="center")
        for row in rows:
            self.tree.insert("", "end", values=row)

    # ------------------------------------------------------------------
    # Resolución de los problemas (reutiliza newt_int, lagrange y
    # biseccion; no se reimplementa ningún método)
    # ------------------------------------------------------------------
    def solve(self):
        try:
            problem = self.problem_option.get()
            if problem == P185:
                self.solve_18_5()
            elif problem == P186:
                self.solve_18_6()
            else:
                self.solve_18_7()
        except Exception as e:
            self.write_box(self.result_box, f"Error al resolver:\n{e}")

    def solve_18_5(self):
        yint, ea = newt_int(X_ORDENADOS, Y_ORDENADOS, XI)

        rows = []
        for k in range(1, len(yint)):
            ea_str = f"{ea[k]:.6f}" if not np.isnan(ea[k]) else "---"
            rows.append((k, f"{yint[k]:.6f}", ea_str))

        self.setup_table(
            [("orden", "Orden", 80),
             ("estimacion", "Estimación f(4)", 160),
             ("error", "Error aprox. (ea)", 160)],
            rows
        )

        result_text = [
            "=== PROBLEMA 18.5 - NEWTON ===",
            "",
            "DATOS USADOS",
            SEP,
            f"Puntos ordenados por cercanía a {XI:g}:",
            f"  x = {X_ORDENADOS}",
            f"  y = {Y_ORDENADOS}",
            "",
            "RESULTADO",
            SEP,
            f"f(4) ≈ {yint[-1]:.6f}   (orden 4)",
            f"Valor verdadero: f(4) = {VALOR_REAL:g}",
            "",
            "(La tabla de la derecha muestra la",
            "estimación y el error de cada orden.)",
            "",
            "INTERPRETACIÓN",
            SEP,
            "El error aproximado se anula a",
            "partir del orden 3 (la diferencia",
            "dividida b4 = 0): los datos",
            "provienen de un polinomio cúbico",
            "(x^3 - x^2 - x + 4), por lo que un",
            "polinomio de orden 3 basta para",
            "interpolar EXACTAMENTE.",
        ]
        self.write_box(self.result_box, "\n".join(result_text))

        # Gráfica: polinomio de mayor orden + datos + punto interpolado.
        xs = np.linspace(0.5, 8.5, 400)
        ys = [newt_int(X_ORDENADOS, Y_ORDENADOS, v)[0][-1] for v in xs]

        self.ax.clear()
        self.ax.plot(xs, ys, label="Polinomio de Newton", linewidth=2)
        self.ax.scatter(X_DATOS, Y_DATOS, label="Datos de la tabla", s=50, zorder=4)
        self.ax.scatter([XI], [yint[-1]], label=f"f(4) = {yint[-1]:.4f}", s=80, zorder=5)
        self.ax.set_title("18.5 — Interpolación de Newton en x = 4")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def solve_18_6(self):
        casos = {
            1: ([3, 5], [19, 99]),
            2: ([2, 3, 5], [6, 19, 99]),
            3: ([2, 3, 5, 7], [6, 19, 99, 291]),
        }

        resultados = {}
        for orden, (xn, yn) in casos.items():
            resultados[orden] = lagrange(xn, yn, XI)

        # Comparación con Newton: el polinomio interpolante es único.
        yint, _ = newt_int(X_ORDENADOS, Y_ORDENADOS, XI)

        rows = []
        for orden, (xn, _) in casos.items():
            rows.append((
                orden,
                str(xn),
                f"{resultados[orden]:.6f}",
                f"{yint[orden]:.6f}",
            ))

        self.setup_table(
            [("orden", "Orden", 70),
             ("nodos", "Nodos", 130),
             ("lagrange", "Lagrange f(4)", 140),
             ("newton", "Newton f(4)", 140)],
            rows
        )

        result_text = [
            "=== PROBLEMA 18.7 - LAGRANGE ===",
            "",
            "RESULTADOS",
            SEP,
            f"Orden 1: f(4) = {resultados[1]:.6f}",
            f"Orden 2: f(4) = {resultados[2]:.6f}",
            f"Orden 3: f(4) = {resultados[3]:.6f}",
            "",
            f"Valor verdadero: f(4) = {VALOR_REAL:g}",
            "",
            "(La tabla de la derecha compara",
            "Lagrange contra Newton por orden.)",
            "",
            "INTERPRETACIÓN",
            SEP,
            "Los resultados de Lagrange son",
            "IDÉNTICOS a los de Newton (18.5)",
            "en cada orden: el polinomio",
            "interpolante de grado n que pasa",
            "por un conjunto de puntos es único.",
            "Newton y Lagrange son dos formas de",
            "escribir el mismo polinomio. Con el",
            "orden 3 se obtiene el valor exacto",
            "(48).",
        ]
        self.write_box(self.result_box, "\n".join(result_text))

        # Gráfica: cúbico de Lagrange (nodos {2,3,5,7}) + datos + f(4).
        xn3, yn3 = casos[3]
        xs = np.linspace(1.5, 7.5, 400)
        ys = [lagrange(xn3, yn3, v) for v in xs]

        self.ax.clear()
        self.ax.plot(xs, ys, label="Polinomio de Lagrange (orden 3)", linewidth=2)
        self.ax.scatter(X_DATOS, Y_DATOS, label="Datos de la tabla", s=50, zorder=4)
        self.ax.scatter(xn3, yn3, label="Nodos usados", s=70, zorder=5, marker="s")
        self.ax.scatter([XI], [resultados[3]], label=f"f(4) = {resultados[3]:.4f}", s=80, zorder=6)
        self.ax.set_title("18.7 — Interpolación de Lagrange en x = 4")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def solve_18_7(self):
        # p(x): cúbico de Newton (estimación de mayor orden).
        # g(x) = p(x) - objetivo: su raíz es el x buscado.
        def p(x):
            return newt_int(X_NODOS_INV, Y_NODOS_INV, x)[0][-1]

        def g(x):
            return p(x) - OBJETIVO

        resultado = biseccion(g, 4.0, 5.0, tol=1e-5, plot_evolution=False)
        raiz = resultado["raiz"]
        x_real = 1 / OBJETIVO  # los datos son f(x) = 1/x

        rows = []
        for it in resultado["iterations"]:
            err = it["error"]
            rows.append((
                it["iter"],
                f"{it['x']:.6f}",
                f"{it['fx']:.6e}",
                "---" if err is None else f"{err:.6e}",
            ))

        self.setup_table(
            [("iter", "Iteración", 80),
             ("x", "x", 130),
             ("gx", "g(x) = p(x) - 0.23", 160),
             ("error", "Error rel.", 130)],
            rows
        )

        result_text = [
            "=== PROBLEMA 18.8 - INT. INVERSA ===",
            "",
            "PLANTEAMIENTO",
            SEP,
            f"Cúbico de Newton, nodos x = {X_NODOS_INV}",
            f"g(4) = {g(4.0):+.4f}",
            f"g(5) = {g(5.0):+.4f}",
            "=> hay cambio de signo en [4, 5].",
            "",
            "RESULTADO (BISECCIÓN)",
            SEP,
            f"Iteraciones: {resultado['iteraciones']}   (tol = 1e-5)",
            f"Solución:    x = {raiz:.6f}",
            "",
            "VERIFICACIÓN",
            SEP,
            f"p({raiz:.4f}) = {p(raiz):.6f}",
            f"Valor real:  1/{OBJETIVO} = {x_real:.6f}",
            f"Diferencia:  {abs(raiz - x_real):.6f}",
            "",
            "INTERPRETACIÓN",
            SEP,
            "La pequeña diferencia se debe al",
            "redondeo de la tabla y a que el",
            "cúbico solo aproxima a 1/x.",
            "La interpolación inversa convierte",
            "un problema sin despeje de x en un",
            "problema de raíces: se combinan",
            "interpolación y bisección.",
        ]
        self.write_box(self.result_box, "\n".join(result_text))

        # Gráfica: p(x), datos de la tabla, recta objetivo y solución.
        xs = np.linspace(2.5, 6.5, 400)
        ys = [p(v) for v in xs]

        self.ax.clear()
        self.ax.plot(xs, ys, label="Cúbico de Newton p(x)", linewidth=2)
        self.ax.scatter(X_INVERSA, Y_INVERSA, label="Datos de la tabla (1/x)", s=50, zorder=4)
        self.ax.axhline(OBJETIVO, linestyle="--", color="gray", label=f"f(x) = {OBJETIVO}")
        self.ax.scatter([raiz], [OBJETIVO], label=f"Solución x = {raiz:.4f}", s=80, zorder=5)
        self.ax.set_title("18.8 — Interpolación inversa (cúbica + bisección)")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def clear_fields(self):
        self.problem_option.set(P185)
        self.update_enunciado(P185)
        self.write_box(self.result_box, "Presione 'Resolver' para ejecutar el problema seleccionado.\n")
        self.clear_table()
        self.reset_plot()
        self.canvas.draw()
