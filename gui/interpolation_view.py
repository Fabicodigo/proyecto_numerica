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

        self.result_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.result_header.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.result_header.grid_columnconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(self.result_header, text="Resultados:")
        self.result_label.grid(row=0, column=0, sticky="w")

        self.expand_button = ctk.CTkButton(
            self.result_header,
            text="Ampliar",
            width=70,
            height=20,
            command=self.expand_results
        )
        self.expand_button.grid(row=0, column=1, sticky="e")

        self.result_box = ctk.CTkTextbox(
            self.left_panel, height=520, wrap="word",
            font=ctk.CTkFont(family="Consolas", size=13)
        )
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

                grado = len(x) - 1
                sep = "-" * 34

                result_text = []
                result_text.append("=== INTERPOLACIÓN DE NEWTON ===")
                result_text.append("")
                result_text.append("DATOS DE ENTRADA")
                result_text.append(sep)
                result_text.append(f"Puntos:      {len(x)}")
                result_text.append(f"Grado máx.:  {grado}")
                result_text.append(f"Interpolar:  xi = {xi}")
                result_text.append("")
                result_text.append("RESULTADO")
                result_text.append(sep)
                result_text.append(f"f({xi:g}) ≈ {yi:.6f}   (grado {grado})")
                result_text.append("")
                result_text.append("EVOLUCIÓN POR GRADO")
                result_text.append(sep)
                result_text.append(f"{'Grado':<6}{'Estimación':>13}{'Error aprox.':>14}")
                for i, val in enumerate(yint):
                    err_str = f"{ea[i]:>14.4e}" if not np.isnan(ea[i]) else f"{'---':>14}"
                    result_text.append(f"{i:<6}{val:>13.6f}{err_str}")

                # Último error aproximado disponible (indica convergencia)
                errores_validos = [e for e in ea if not np.isnan(e)]
                result_text.append("")
                result_text.append("INTERPRETACIÓN")
                result_text.append(sep)
                if errores_validos:
                    result_text.append(f"Último error aprox.: {errores_validos[-1]:.4e}")
                    result_text.append("")
                result_text.append("El error ea[k] mide cuánto cambia")
                result_text.append("la estimación al subir un grado:")
                result_text.append("si se anula, agregar más puntos ya")
                result_text.append("no mejora la interpolación.")

                self.write_result("\n".join(result_text))
                self.plot_interpolation(method, x, y, xi, yi)

            elif method == "Lagrange":
                yi = self.eval_lagrange(x, y, xi)

                grado = len(x) - 1
                sep = "-" * 34

                result_text = []
                result_text.append("=== INTERPOLACIÓN DE LAGRANGE ===")
                result_text.append("")
                result_text.append("DATOS DE ENTRADA")
                result_text.append(sep)
                result_text.append(f"Puntos:      {len(x)}")
                result_text.append(f"Grado:       {grado}")
                result_text.append(f"Interpolar:  xi = {xi}")
                result_text.append("")
                result_text.append("RESULTADO")
                result_text.append(sep)
                result_text.append(f"f({xi:g}) ≈ {yi:.6f}   (grado {grado})")
                result_text.append("")

                # Verificación cruzada: el polinomio interpolante es único,
                # por lo que Newton con los mismos puntos debe coincidir.
                yint_newton, _ = newt_int(x, y, xi)
                dif = abs(yi - yint_newton[-1])
                result_text.append("VERIFICACIÓN CON NEWTON")
                result_text.append(sep)
                result_text.append(f"Lagrange:    {yi:.6f}")
                result_text.append(f"Newton:      {yint_newton[-1]:.6f}")
                result_text.append(f"Diferencia:  {dif:.2e}")
                result_text.append("")
                result_text.append("Coinciden porque el polinomio")
                result_text.append("interpolante que pasa por un conjunto")
                result_text.append("de puntos es único: Newton y Lagrange")
                result_text.append("son dos formas de escribir el mismo")
                result_text.append("polinomio.")

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

    def expand_results(self):
        content = self.result_box.get("1.0", "end-1c")
        
        popup = ctk.CTkToplevel(self)
        popup.title("Resumen Ampliado")
        popup.geometry("800x600")
        
        popup.update_idletasks()
        width = 800
        height = 600
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        
        textbox = ctk.CTkTextbox(popup, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        textbox.insert("1.0", content)
        textbox.configure(state="disabled")
        
        close_btn = ctk.CTkButton(popup, text="Cerrar", command=popup.destroy)
        close_btn.grid(row=1, column=0, padx=20, pady=(0, 20))