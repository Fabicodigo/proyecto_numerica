import customtkinter as ctk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.parser import construir_funcion
from codigo.trapecio import trapm_func
from codigo.simpson import simp_int_func


class IntegrationView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo
        self.left_panel = ctk.CTkScrollableFrame(self)
        self.left_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Panel derecho
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        # ===== IZQUIERDA =====
        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="Módulo de Integración Numérica",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.method_label = ctk.CTkLabel(self.left_panel, text="Método:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.method_option = ctk.CTkOptionMenu(
            self.left_panel,
            values=["Trapecio", "Simpson"]
        )
        self.method_option.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.func_label = ctk.CTkLabel(self.left_panel, text="Función f(x):")
        self.func_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.func_entry = ctk.CTkEntry(
            self.left_panel,
            placeholder_text="Ejemplo: x**2, sin(x), exp(x)"
        )
        self.func_entry.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.a_label = ctk.CTkLabel(self.left_panel, text="Límite inferior a:")
        self.a_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        self.a_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 0")
        self.a_entry.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.b_label = ctk.CTkLabel(self.left_panel, text="Límite superior b:")
        self.b_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")

        self.b_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 2")
        self.b_entry.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        self.n_label = ctk.CTkLabel(self.left_panel, text="Número de segmentos n:")
        self.n_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")

        self.n_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 4")
        self.n_entry.grid(row=10, column=0, padx=20, pady=5, sticky="ew")

        self.buttons_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.buttons_frame.grid(row=11, column=0, padx=20, pady=15, sticky="ew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.calculate_button = ctk.CTkButton(
            self.buttons_frame,
            text="Calcular",
            command=self.calculate
        )
        self.calculate_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Limpiar",
            fg_color="gray40",
            hover_color="gray30",
            command=self.clear_fields
        )
        self.clear_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        self.result_label = ctk.CTkLabel(self.left_panel, text="Resultados:")
        self.result_label.grid(row=12, column=0, padx=20, pady=(10, 0), sticky="w")

        self.result_box = ctk.CTkTextbox(self.left_panel, height=230)
        self.result_box.grid(row=13, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.result_box.insert("1.0", "Aquí aparecerán los resultados...\n")
        self.result_box.configure(state="disabled")

        # ===== DERECHA =====
        self.graph_title = ctk.CTkLabel(
            self.right_panel,
            text="Gráfica de Integración",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.graph_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Función e integral aproximada")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.canvas.draw()

    def write_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def plot_integration(self, func, a, b, n, method, result):
        xs = np.linspace(a, b, 400)
        ys = func(xs)

        xn = np.linspace(a, b, n + 1)
        yn = func(xn)

        self.ax.clear()
        self.ax.plot(xs, ys, label="f(x)", linewidth=2)
        self.ax.scatter(xn, yn, label="Nodos", s=35)

        self.ax.fill_between(xs, ys, 0, alpha=0.25, label=f"Área aproximada ({method})")

        if method == "Trapecio":
            for i in range(len(xn) - 1):
                self.ax.plot([xn[i], xn[i + 1]], [yn[i], yn[i + 1]], linewidth=1.5)
                self.ax.vlines([xn[i], xn[i + 1]], 0, [yn[i], yn[i + 1]], linestyles="dashed", alpha=0.5)

        self.ax.set_title(f"{method} | Integral ≈ {result:.6f}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def calculate(self):
        try:
            method = self.method_option.get()
            expr = self.func_entry.get().strip()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())

            if expr == "":
                self.write_result("Error: debe ingresar una función.")
                return

            if a >= b:
                self.write_result("Error: el límite inferior a debe ser menor que b.")
                return

            if n <= 0:
                self.write_result("Error: n debe ser un entero positivo.")
                return

            func = construir_funcion(expr)

            if method == "Trapecio":
                result = trapm_func(func, a, b, n)

                result_text = []
                result_text.append("=== REGLA DEL TRAPECIO ===\n")
                result_text.append(f"f(x) = {expr}")
                result_text.append(f"Intervalo: [{a}, {b}]")
                result_text.append(f"n = {n}")
                result_text.append(f"Integral aproximada = {result:.6f}")

                self.write_result("\n".join(result_text))
                self.plot_integration(func, a, b, n, method, result)

            elif method == "Simpson":
                result = simp_int_func(func, a, b, n)

                result_text = []
                result_text.append("=== REGLA DE SIMPSON ===\n")
                result_text.append(f"f(x) = {expr}")
                result_text.append(f"Intervalo: [{a}, {b}]")
                result_text.append(f"n = {n}")
                result_text.append(f"Integral aproximada = {result:.6f}")

                self.write_result("\n".join(result_text))
                self.plot_integration(func, a, b, n, method, result)

        except Exception as e:
            self.write_result(f"Error al calcular:\n{e}")

    def clear_fields(self):
        self.func_entry.delete(0, "end")
        self.a_entry.delete(0, "end")
        self.b_entry.delete(0, "end")
        self.n_entry.delete(0, "end")
        self.method_option.set("Trapecio")
        self.write_result("Aquí aparecerán los resultados...\n")

        self.ax.clear()
        self.ax.set_title("Función e integral aproximada")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()