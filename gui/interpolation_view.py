import customtkinter as ctk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from codigo.newton_interpolacion import newt_int
from codigo.lagrange_interpolacion import lagrange


class InterpolationView(ctk.CTkFrame):
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

        # ===== IZQUIERDA: formulario =====
        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="Módulo de Interpolación",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.method_label = ctk.CTkLabel(self.left_panel, text="Método:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.method_option = ctk.CTkOptionMenu(
            self.left_panel,
            values=["Newton", "Lagrange"]
        )
        self.method_option.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.x_label = ctk.CTkLabel(self.left_panel, text="Valores de x (separados por espacios):")
        self.x_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.x_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 1 2 3")
        self.x_entry.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.y_label = ctk.CTkLabel(self.left_panel, text="Valores de y (separados por espacios):")
        self.y_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        self.y_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 1 4 9")
        self.y_entry.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.xi_label = ctk.CTkLabel(self.left_panel, text="Valor xi a interpolar:")
        self.xi_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")

        self.xi_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 2.5")
        self.xi_entry.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        self.buttons_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.buttons_frame.grid(row=9, column=0, padx=20, pady=15, sticky="ew")
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
        self.result_label.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="w")

        self.result_box = ctk.CTkTextbox(self.left_panel, height=250)
        self.result_box.grid(row=11, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.result_box.insert("1.0", "Aquí aparecerán los resultados...\n")
        self.result_box.configure(state="disabled")

        # ===== DERECHA: gráfica =====
        self.graph_title = ctk.CTkLabel(
            self.right_panel,
            text="Gráfica de Interpolación",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.graph_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Datos e interpolación")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="nsew")

        self.canvas.draw()

    def parse_list(self, text):
        return [float(v) for v in text.strip().split()]

    def write_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def eval_newton(self, x, y, x_value):
        yint, _ = newt_int(x, y, x_value)
        return yint[-1]

    def eval_lagrange(self, x, y, x_value):
        return lagrange(x, y, x_value)

    def plot_interpolation(self, method, x, y, xi, yi):
        x_min = min(min(x), xi)
        x_max = max(max(x), xi)

        if x_min == x_max:
            x_min -= 1
            x_max += 1

        margen = (x_max - x_min) * 0.1
        xs = np.linspace(x_min - margen, x_max + margen, 300)

        if method == "Newton":
            ys = [self.eval_newton(x, y, val) for val in xs]
        else:
            ys = [self.eval_lagrange(x, y, val) for val in xs]

        self.ax.clear()
        self.ax.plot(xs, ys, label=f"Interpolación {method}", linewidth=2)
        self.ax.scatter(x, y, label="Datos originales", s=50)
        self.ax.scatter([xi], [yi], label=f"Punto interpolado ({xi}, {round(yi, 4)})", s=70)
        self.ax.set_title("Datos e interpolación")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def calculate(self):
        try:
            method = self.method_option.get()
            x = self.parse_list(self.x_entry.get())
            y = self.parse_list(self.y_entry.get())
            xi = float(self.xi_entry.get())

            if len(x) != len(y):
                self.write_result("Error: x e y deben tener la misma cantidad de elementos.")
                return

            if len(x) < 2:
                self.write_result("Error: debe ingresar al menos 2 puntos.")
                return

            if len(set(x)) != len(x):
                self.write_result("Error: los valores de x no deben repetirse.")
                return

            if method == "Newton":
                yint, ea = newt_int(x, y, xi)
                yi = yint[-1]

                result_text = []
                result_text.append("=== INTERPOLACIÓN DE NEWTON ===\n")
                result_text.append(f"xi = {xi}")
                result_text.append(f"Resultado final = {yi:.6f}\n")
                result_text.append("Evolución por grado:")
                for i, val in enumerate(yint):
                    result_text.append(f"  Grado {i}: {val:.6f}")
                result_text.append("\nErrores aproximados:")
                for i, err in enumerate(ea):
                    result_text.append(f"  Error grado {i}: {err}")

                self.write_result("\n".join(result_text))
                self.plot_interpolation(method, x, y, xi, yi)

            elif method == "Lagrange":
                yi = self.eval_lagrange(x, y, xi)

                result_text = []
                result_text.append("=== INTERPOLACIÓN DE LAGRANGE ===\n")
                result_text.append(f"xi = {xi}")
                result_text.append(f"Resultado final = {yi:.6f}")

                self.write_result("\n".join(result_text))
                self.plot_interpolation(method, x, y, xi, yi)

        except Exception as e:
            self.write_result(f"Error al calcular:\n{e}")

    def clear_fields(self):
        self.x_entry.delete(0, "end")
        self.y_entry.delete(0, "end")
        self.xi_entry.delete(0, "end")
        self.method_option.set("Newton")
        self.write_result("Aquí aparecerán los resultados...\n")

        self.ax.clear()
        self.ax.set_title("Datos e interpolación")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()