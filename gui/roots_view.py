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
        self.left_panel = ctk.CTkScrollableFrame(self)
        self.left_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Panel derecho
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(4, weight=1)

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

        self.result_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.result_header.grid(row=18, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.result_header.grid_columnconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(self.result_header, text="Resumen:")
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

        # Controles de Animación/Simulación
        self.controls_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_prev = ctk.CTkButton(
            self.controls_frame,
            text="Atrás",
            width=80,
            command=self.anim_step_backward,
            state="disabled"
        )
        self.btn_prev.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_play = ctk.CTkButton(
            self.controls_frame,
            text="Reproducir",
            width=100,
            command=self.anim_play_pause,
            state="disabled"
        )
        self.btn_play.grid(row=0, column=1, padx=5, sticky="ew")

        self.btn_next = ctk.CTkButton(
            self.controls_frame,
            text="Adelante",
            width=80,
            command=self.anim_step_forward,
            state="disabled"
        )
        self.btn_next.grid(row=0, column=2, padx=5, sticky="ew")

        self.table_title = ctk.CTkLabel(
            self.right_panel,
            text="Tabla de Iteraciones",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.table_title.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="w")

        table_frame = ctk.CTkFrame(self.right_panel)
        table_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
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

        self.animation_id = None
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

    def start_animation(self, func, domain_min, domain_max, iterations, root, method):
        if hasattr(self, "animation_id") and self.animation_id is not None:
            self.after_cancel(self.animation_id)
            self.animation_id = None

        self.clear_table()

        self.anim_func = func
        self.anim_domain_min = domain_min
        self.anim_domain_max = domain_max
        self.anim_iterations = iterations
        self.anim_root = root
        self.anim_method = method

        self.anim_current_idx = 0
        self.anim_x_iters = []
        self.anim_y_iters = []
        self.anim_scatter_plot = None
        self.anim_is_playing = False

        xs = np.linspace(domain_min, domain_max, 400)
        ys = func(xs)
        self.ax.clear()
        self.ax.plot(xs, ys, label="f(x)", linewidth=2, color="#1f77b4")
        self.ax.axhline(0, color="gray", linewidth=1, linestyle="--")
        self.ax.set_title(f"{method} - Evolución en tiempo real")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

        self.btn_prev.configure(state="disabled")
        self.btn_play.configure(state="normal", text="Pausar")
        self.btn_next.configure(state="normal")

        self.anim_is_playing = True
        self.anim_step()

    def anim_play_pause(self):
        if not hasattr(self, "anim_iterations") or not self.anim_iterations:
            return

        if self.anim_is_playing:
            self.anim_is_playing = False
            self.btn_play.configure(text="Reproducir")
            if self.animation_id is not None:
                self.after_cancel(self.animation_id)
                self.animation_id = None
        else:
            self.anim_is_playing = True
            self.btn_play.configure(text="Pausar")
            self.anim_step()

    def anim_step(self):
        if not self.anim_is_playing:
            return

        if self.anim_current_idx >= len(self.anim_iterations):
            self.anim_is_playing = False
            self.btn_play.configure(text="Reproducir", state="disabled")
            self.btn_next.configure(state="disabled")
            return

        self.anim_step_forward()
        self.animation_id = self.after(300, self.anim_step)

    def anim_step_forward(self):
        if not hasattr(self, "anim_iterations") or self.anim_current_idx >= len(self.anim_iterations):
            return

        it = self.anim_iterations[self.anim_current_idx]

        iter_num = it.get("iter", "")
        x_val = it.get("x", "")
        fx_val = it.get("fx", "")
        error_val = it.get("error", "")

        x_str = f"{x_val:.6f}" if isinstance(x_val, (int, float)) else str(x_val)
        fx_str = f"{fx_val:.6f}" if isinstance(fx_val, (int, float)) else str(fx_val)
        err_str = f"{error_val:.6e}" if isinstance(error_val, (int, float)) else str(error_val)

        self.tree.insert("", "end", values=(iter_num, x_str, fx_str, err_str))
        self.tree.yview_moveto(1.0)

        self.anim_x_iters.append(x_val)
        self.anim_y_iters.append(fx_val)

        if self.anim_scatter_plot is not None:
            self.anim_scatter_plot.remove()

        self.anim_scatter_plot = self.ax.scatter(self.anim_x_iters, self.anim_y_iters, color="#ff7f0e", s=45, label="Iterados", zorder=4)

        self.anim_current_idx += 1

        if self.anim_current_idx == len(self.anim_iterations):
            if self.anim_root is not None:
                try:
                    y_root = self.anim_func(self.anim_root)
                    self.ax.scatter([self.anim_root], [y_root], label=f"Raíz ({round(self.anim_root, 6)})", color="#d62728", s=80, zorder=5)
                except Exception:
                    pass
            self.btn_play.configure(text="Reproducir", state="disabled")
            self.btn_next.configure(state="disabled")

        self.btn_prev.configure(state="normal")
        self.ax.legend()
        self.canvas.draw()

    def anim_step_backward(self):
        if not hasattr(self, "anim_iterations") or self.anim_current_idx <= 0:
            return

        if self.anim_is_playing:
            self.anim_play_pause()

        self.anim_current_idx -= 1
        self.anim_x_iters.pop()
        self.anim_y_iters.pop()

        children = self.tree.get_children()
        if children:
            self.tree.delete(children[-1])

        xs = np.linspace(self.anim_domain_min, self.anim_domain_max, 400)
        ys = self.anim_func(xs)
        self.ax.clear()
        self.ax.plot(xs, ys, label="f(x)", linewidth=2, color="#1f77b4")
        self.ax.axhline(0, color="gray", linewidth=1, linestyle="--")
        self.ax.set_title(f"{self.anim_method} - Evolución en tiempo real")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)

        if self.anim_x_iters:
            self.anim_scatter_plot = self.ax.scatter(self.anim_x_iters, self.anim_y_iters, color="#ff7f0e", s=45, label="Iterados", zorder=4)
        else:
            self.anim_scatter_plot = None

        self.ax.legend()
        self.canvas.draw()

        self.btn_next.configure(state="normal")
        self.btn_play.configure(state="normal")

        if self.anim_current_idx == 0:
            self.btn_prev.configure(state="disabled")

    def calculate(self):
        try:
            method = self.method_option.get()
            expr = self.func_entry.get().strip()

            if expr == "":
                self.write_result("Error: Debe ingresar una función f(x). Ejemplo: x**3 - x - 2")
                return

            try:
                func = construir_funcion(expr)
            except Exception as e:
                self.write_result(f"Error: La función ingresada no es válida.\n{e}")
                return

            try:
                tol = float(self.tol_entry.get())
            except ValueError:
                self.write_result("Error: Ingrese valores numéricos válidos en todos los campos visibles.")
                return

            try:
                domain_min = float(self.domain_min_entry.get())
                domain_max = float(self.domain_max_entry.get())
            except ValueError:
                self.write_result("Error: Debe ingresar un dominio gráfico válido.")
                return

            if domain_min >= domain_max:
                self.write_result("Error: El dominio gráfico mínimo debe ser menor que el máximo.")
                return

            if method == "Bisección":
                try:
                    a = float(self.param1_entry.get())
                    b = float(self.param2_entry.get())
                except ValueError:
                    self.write_result("Error: Ingrese valores numéricos válidos en todos los campos visibles.")
                    return

                try:
                    result = biseccion(func, a, b, tol=tol, max_iter=150, plot_evolution=False)
                except ValueError as e:
                    if "signos opuestos" in str(e) or "Bolzano" in str(e):
                        self.write_result("Error: En Bisección, los extremos deben encerrar un cambio de signo.")
                        return
                    raise e

                config_lines = [f"Intervalo:   [{a}, {b}]"]

            elif method == "Newton":
                d_expr = self.dfunc_entry.get().strip()
                if d_expr == "":
                    self.write_result("Error: Newton requiere la derivada f'(x). Ejemplo: 3*x**2 - 1")
                    return

                try:
                    dfunc = construir_funcion(d_expr)
                except Exception as e:
                    self.write_result(f"Error: La derivada ingresada no es válida.\n{e}")
                    return

                try:
                    x0 = float(self.param1_entry.get())
                except ValueError:
                    self.write_result("Error: Ingrese valores numéricos válidos en todos los campos visibles.")
                    return

                result = newton(func, dfunc, x0, tol=tol, max_iter=150, plot_evolution=False, domain_grafico=(domain_min, domain_max))

                config_lines = [
                    f"Derivada:    f'(x) = {d_expr}",
                    f"x0 inicial:  {x0}",
                ]

            elif method == "Secante":
                try:
                    x0 = float(self.param1_entry.get())
                    x1 = float(self.param2_entry.get())
                except ValueError:
                    self.write_result("Error: Ingrese valores numéricos válidos en todos los campos visibles.")
                    return

                result = secante(func, x0, x1, tol=tol, max_iter=150, plot_evolution=False, domain_grafico=(domain_min, domain_max))

                config_lines = [f"Iniciales:   x0 = {x0}, x1 = {x1}"]

            self.start_animation(func, domain_min, domain_max, result["iterations"], result.get("root"), method)

            iterations = result.get("iterations", [])
            root = result.get("root")
            f_root = result.get("f_root")

            # Último error relativo aproximado registrado
            last_err = None
            for it in reversed(iterations):
                if it.get("error") is not None:
                    last_err = it["error"]
                    break

            sep = "-" * 34

            summary = []
            summary.append(f"====== {method.upper()} ======")
            summary.append("")
            summary.append("DATOS DE ENTRADA")
            summary.append(sep)
            summary.append(f"Función:     f(x) = {expr}")
            summary.extend(config_lines)
            summary.append(f"Tolerancia:  {tol:g}")
            summary.append("Máx. iter.:  150")
            summary.append("")
            summary.append("RESULTADOS")
            summary.append(sep)
            summary.append(f"Estado:      {result.get('message', 'Sin mensaje')}")
            summary.append(f"Convergió:   {'Sí' if result.get('success') else 'No'}")
            summary.append(f"Iteraciones: {len(iterations)}")
            if isinstance(root, (int, float)):
                summary.append(f"Raíz:        x = {root:.10f}")
            else:
                summary.append(f"Raíz:        {root}")
            if isinstance(f_root, (int, float)):
                summary.append(f"f(raíz):     {f_root:.6e}")
            else:
                summary.append(f"f(raíz):     {f_root}")
            if last_err is not None:
                summary.append(f"Error final: {last_err:.6e}")
            else:
                summary.append("Error final: N/A (una sola iteración)")

            if isinstance(f_root, (int, float)):
                cumple = abs(f_root) <= tol
                summary.append("")
                summary.append("VERIFICACIÓN")
                summary.append(sep)
                summary.append(f"|f(raíz)| = {abs(f_root):.6e}")
                summary.append(f"tolerancia = {tol:g}")
                if cumple:
                    summary.append("=> |f(raíz)| <= tol:")
                    summary.append("   la raíz satisface la tolerancia.")
                else:
                    summary.append("=> |f(raíz)| > tol:")
                    summary.append("   convergió por error relativo,")
                    summary.append("   no por el valor de |f(x)|.")

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
        if hasattr(self, "animation_id") and self.animation_id is not None:
            self.after_cancel(self.animation_id)
            self.animation_id = None

        if hasattr(self, "anim_iterations"):
            self.anim_iterations = []

        self.btn_prev.configure(state="disabled")
        self.btn_play.configure(state="disabled", text="Reproducir")
        self.btn_next.configure(state="disabled")

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