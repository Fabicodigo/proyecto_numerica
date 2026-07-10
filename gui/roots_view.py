import customtkinter as ctk
import numpy as np
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.parser import construir_funcion
from codigo.biseccion import biseccion
from codigo.newton_raices import newton
from codigo.secante import secante


class RootsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Panel derecho
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(3, weight=1)

        # ===== IZQUIERDA =====
        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="Módulo de Métodos de Raíces",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.method_label = ctk.CTkLabel(self.left_panel, text="Método:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.method_option = ctk.CTkOptionMenu(
            self.left_panel,
            values=["Bisección", "Newton", "Secante"],
            command=self.update_fields
        )
        self.method_option.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.func_label = ctk.CTkLabel(self.left_panel, text="Función f(x):")
        self.func_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.func_entry = ctk.CTkEntry(
            self.left_panel,
            placeholder_text="Ejemplo: x**3 - x - 1"
        )
        self.func_entry.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.dfunc_label = ctk.CTkLabel(self.left_panel, text="Derivada f'(x):")
        self.dfunc_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        self.dfunc_entry = ctk.CTkEntry(
            self.left_panel,
            placeholder_text="Solo para Newton. Ejemplo: 3*x**2 - 1"
        )
        self.dfunc_entry.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.param1_label = ctk.CTkLabel(self.left_panel, text="Parámetro 1:")
        self.param1_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")

        self.param1_entry = ctk.CTkEntry(self.left_panel)
        self.param1_entry.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        self.param2_label = ctk.CTkLabel(self.left_panel, text="Parámetro 2:")
        self.param2_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")

        self.param2_entry = ctk.CTkEntry(self.left_panel)
        self.param2_entry.grid(row=10, column=0, padx=20, pady=5, sticky="ew")

        self.domain_min_label = ctk.CTkLabel(self.left_panel, text="Dominio gráfico mínimo:")
        self.domain_min_label.grid(row=11, column=0, padx=20, pady=(10, 0), sticky="w")

        self.domain_min_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: -5")
        self.domain_min_entry.grid(row=12, column=0, padx=20, pady=5, sticky="ew")

        self.domain_max_label = ctk.CTkLabel(self.left_panel, text="Dominio gráfico máximo:")
        self.domain_max_label.grid(row=13, column=0, padx=20, pady=(10, 0), sticky="w")

        self.domain_max_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 5")
        self.domain_max_entry.grid(row=14, column=0, padx=20, pady=5, sticky="ew")

        self.tol_label = ctk.CTkLabel(self.left_panel, text="Tolerancia:")
        self.tol_label.grid(row=15, column=0, padx=20, pady=(10, 0), sticky="w")

        self.tol_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 1e-6")
        self.tol_entry.grid(row=16, column=0, padx=20, pady=5, sticky="ew")
        self.tol_entry.insert(0, "1e-6")

        self.buttons_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.buttons_frame.grid(row=17, column=0, padx=20, pady=15, sticky="ew")
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

        self.result_label = ctk.CTkLabel(self.left_panel, text="Resumen:")
        self.result_label.grid(row=18, column=0, padx=20, pady=(10, 0), sticky="w")

        self.result_box = ctk.CTkTextbox(self.left_panel, height=180)
        self.result_box.grid(row=19, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.result_box.insert("1.0", "Aquí aparecerá el resumen del método.\n")
        self.result_box.configure(state="disabled")

        # ===== DERECHA =====
        self.graph_title = ctk.CTkLabel(
            self.right_panel,
            text="Gráfica del Método",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.graph_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Función e iterados")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.canvas.draw()

        self.table_title = ctk.CTkLabel(
            self.right_panel,
            text="Tabla de Iteraciones",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.table_title.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="w")

        table_frame = ctk.CTkFrame(self.right_panel)
        table_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("iter", "x", "fx", "error"),
            show="headings",
            height=10
        )
        self.tree.heading("iter", text="Iteración")
        self.tree.heading("x", text="x")
        self.tree.heading("fx", text="f(x)")
        self.tree.heading("error", text="Error")

        self.tree.column("iter", width=80, anchor="center")
        self.tree.column("x", width=120, anchor="center")
        self.tree.column("fx", width=120, anchor="center")
        self.tree.column("error", width=120, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.update_fields("Bisección")

    def write_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def update_fields(self, method):
        if method == "Bisección":
            self.dfunc_label.grid_remove()
            self.dfunc_entry.grid_remove()

            self.param1_label.configure(text="Extremo izquierdo a:")
            self.param2_label.configure(text="Extremo derecho b:")

            self.domain_min_label.configure(text="Dominio gráfico mínimo:")
            self.domain_max_label.configure(text="Dominio gráfico máximo:")

        elif method == "Newton":
            self.dfunc_label.grid()
            self.dfunc_entry.grid()

            self.param1_label.configure(text="Aproximación inicial x0:")
            self.param2_label.configure(text="(No aplica)")

            self.domain_min_label.configure(text="Dominio gráfico mínimo:")
            self.domain_max_label.configure(text="Dominio gráfico máximo:")

        elif method == "Secante":
            self.dfunc_label.grid_remove()
            self.dfunc_entry.grid_remove()

            self.param1_label.configure(text="Valor inicial x0:")
            self.param2_label.configure(text="Valor inicial x1:")

            self.domain_min_label.configure(text="Dominio gráfico mínimo:")
            self.domain_max_label.configure(text="Dominio gráfico máximo:")

    def plot_method(self, func, domain_min, domain_max, iterations, root, method):
        xs = np.linspace(domain_min, domain_max, 400)
        ys = func(xs)

        self.ax.clear()
        self.ax.plot(xs, ys, label="f(x)", linewidth=2)
        self.ax.axhline(0, linewidth=1)

        x_iters = [it["x"] for it in iterations]
        y_iters = [it["fx"] for it in iterations]

        self.ax.scatter(x_iters, y_iters, label="Iterados", s=45)

        if root is not None:
            try:
                y_root = func(root)
                self.ax.scatter([root], [y_root], label=f"Raíz aproximada ({round(root, 6)})", s=70)
            except Exception:
                pass

        self.ax.set_title(f"{method} - Evolución gráfica")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def fill_table(self, iterations):
        self.clear_table()

        for it in iterations:
            iter_num = it.get("iter", "")
            x = it.get("x", "")
            fx = it.get("fx", "")
            error = it.get("error", "")

            if isinstance(x, (int, float)):
                x = f"{x:.6f}"
            if isinstance(fx, (int, float)):
                fx = f"{fx:.6f}"
            if isinstance(error, (int, float)):
                error = f"{error:.6e}"

            self.tree.insert("", "end", values=(iter_num, x, fx, error))

    def calculate(self):
        try:
            method = self.method_option.get()
            expr = self.func_entry.get().strip()

            if expr == "":
                self.write_result("Error: debe ingresar una función.")
                return

            func = construir_funcion(expr)
            tol = float(self.tol_entry.get())

            domain_min = float(self.domain_min_entry.get())
            domain_max = float(self.domain_max_entry.get())

            if domain_min >= domain_max:
                self.write_result("Error: el dominio gráfico mínimo debe ser menor que el máximo.")
                return

            if method == "Bisección":
                a = float(self.param1_entry.get())
                b = float(self.param2_entry.get())

                result = biseccion(func, a, b, tol=tol, max_iter=150)

            elif method == "Newton":
                d_expr = self.dfunc_entry.get().strip()
                if d_expr == "":
                    self.write_result("Error: en Newton debe ingresar la derivada f'(x).")
                    return

                dfunc = construir_funcion(d_expr)
                x0 = float(self.param1_entry.get())

                result = newton(func, dfunc, x0, tol=tol, max_iter=150)

            elif method == "Secante":
                x0 = float(self.param1_entry.get())
                x1 = float(self.param2_entry.get())

                result = secante(func, x0, x1, tol=tol, max_iter=150)

            self.fill_table(result["iterations"])
            self.plot_method(func, domain_min, domain_max, result["iterations"], result.get("root"), method)

            summary = []
            summary.append(f"=== {method.upper()} ===\n")
            summary.append(f"Estado: {result.get('message', 'Sin mensaje')}")
            summary.append(f"Raíz aproximada: {result.get('root', 'N/A')}")
            summary.append(f"f(raíz): {result.get('f_root', 'N/A')}")
            summary.append(f"Iteraciones: {len(result.get('iterations', []))}")

            self.write_result("\n".join(map(str, summary)))

        except NotImplementedError:
            self.write_result(
                "El método todavía no está integrado.\n\n"
                "Pídele al compañero de raíces que devuelva un diccionario con este formato:\n"
                "{\n"
                '  "success": True,\n'
                '  "message": "Convergió por tolerancia",\n'
                '  "root": 2.0,\n'
                '  "f_root": 0.0,\n'
                '  "iterations": [\n'
                '       {"iter": 1, "x": 1.5, "fx": -1.75, "error": None}\n'
                "  ]\n"
                "}"
            )
        except Exception as e:
            self.write_result(f"Error al calcular:\n{e}")

    def clear_fields(self):
        self.func_entry.delete(0, "end")
        self.dfunc_entry.delete(0, "end")
        self.param1_entry.delete(0, "end")
        self.param2_entry.delete(0, "end")
        self.domain_min_entry.delete(0, "end")
        self.domain_max_entry.delete(0, "end")
        self.tol_entry.delete(0, "end")
        self.tol_entry.insert(0, "1e-6")
        self.method_option.set("Bisección")
        self.update_fields("Bisección")

        self.write_result("Aquí aparecerá el resumen del método.\n")
        self.clear_table()

        self.ax.clear()
        self.ax.set_title("Función e iterados")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()