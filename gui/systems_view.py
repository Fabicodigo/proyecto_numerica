import customtkinter as ctk
import numpy as np
from tkinter import ttk

from codigo.gauss_pivoteo import gauss_pivoteo_parcial
from codigo.gauss_seidel import gauss_seidel, check_diagonal_dominance


class SystemsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1, minsize=420)
        self.grid_columnconfigure(1, weight=2)
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
        self.right_panel.grid_rowconfigure(3, weight=1)

        # ===== IZQUIERDA =====
        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="Módulo de Sistemas Lineales",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.method_label = ctk.CTkLabel(self.left_panel, text="Método:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.method_option = ctk.CTkOptionMenu(
            self.left_panel,
            values=["Gauss con pivoteo parcial", "Gauss-Seidel"],
            command=self.update_fields
        )
        self.method_option.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.matrix_label = ctk.CTkLabel(self.left_panel, text="Matriz A (una fila por línea, valores separados por espacios):")
        self.matrix_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.matrix_box = ctk.CTkTextbox(self.left_panel, height=120)
        self.matrix_box.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.matrix_box.insert("1.0", "4 1\n2 3")

        self.vector_label = ctk.CTkLabel(self.left_panel, text="Vector b (valores separados por espacios):")
        self.vector_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        self.vector_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 1 2")
        self.vector_entry.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        self.vector_entry.insert(0, "1 2")

        self.x0_label = ctk.CTkLabel(self.left_panel, text="Vector inicial x0 (solo para Gauss-Seidel):")
        self.x0_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")

        self.x0_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 0 0")
        self.x0_entry.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        self.tol_label = ctk.CTkLabel(self.left_panel, text="Tolerancia (solo para Gauss-Seidel):")
        self.tol_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")

        self.tol_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Ejemplo: 1e-6")
        self.tol_entry.grid(row=10, column=0, padx=20, pady=5, sticky="ew")
        self.tol_entry.insert(0, "1e-6")

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

        self.result_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.result_header.grid(row=12, column=0, padx=20, pady=(10, 0), sticky="ew")
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
        self.result_box.grid(row=13, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.result_box.insert("1.0", "Aquí aparecerá el resumen del método.\n")
        self.result_box.configure(state="disabled")

        # ===== DERECHA =====
        self.table_title = ctk.CTkLabel(
            self.right_panel,
            text="Resultados / Iteraciones",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.table_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        table_frame = ctk.CTkFrame(self.right_panel)
        table_frame.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, show="headings", height=14)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.update_fields("Gauss con pivoteo parcial")

    def write_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def clear_table(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()

    def parse_matrix(self):
        content = self.matrix_box.get("1.0", "end").strip()
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        if not lines:
            raise ValueError("Debe ingresar la matriz A.")

        matrix = []
        expected_len = None

        for line in lines:
            row = [float(x) for x in line.split()]
            if expected_len is None:
                expected_len = len(row)
            elif len(row) != expected_len:
                raise ValueError("Todas las filas de la matriz A deben tener la misma cantidad de elementos.")
            matrix.append(row)

        if len(matrix) != expected_len:
            raise ValueError("La matriz A debe ser cuadrada.")

        return matrix

    def parse_vector(self, text, expected_len, field_name="vector"):
        values = [float(x) for x in text.strip().split()]
        if len(values) != expected_len:
            raise ValueError(f"El {field_name} debe tener exactamente {expected_len} elementos.")
        return values

    def setup_solution_table(self, solution):
        self.clear_table()

        n = len(solution)
        columns = ("variable", "valor")
        self.tree["columns"] = columns

        self.tree.heading("variable", text="Variable")
        self.tree.heading("valor", text="Valor")

        self.tree.column("variable", width=120, anchor="center")
        self.tree.column("valor", width=180, anchor="center")

        for i, value in enumerate(solution, start=1):
            if isinstance(value, (int, float)):
                value = f"{value:.6f}"
            self.tree.insert("", "end", values=(f"x{i}", value))

    def setup_iterations_table(self, iterations):
        self.clear_table()

        if not iterations:
            return

        first = iterations[0]
        x_values = first.get("x", [])

        if not isinstance(x_values, (list, tuple)):
            x_values = [x_values]

        columns = ["iter"] + [f"x{i+1}" for i in range(len(x_values))] + ["error"]
        self.tree["columns"] = columns

        self.tree.heading("iter", text="Iteración")
        self.tree.column("iter", width=80, anchor="center")

        for i in range(len(x_values)):
            col = f"x{i+1}"
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")

        self.tree.heading("error", text="Error")
        self.tree.column("error", width=120, anchor="center")

        for it in iterations:
            row = [it.get("iter", "")]

            xs = it.get("x", [])
            if not isinstance(xs, (list, tuple)):
                xs = [xs]

            for val in xs:
                if isinstance(val, (int, float)):
                    row.append(f"{val:.6f}")
                else:
                    row.append(str(val))

            error = it.get("error", "")
            if isinstance(error, (int, float)):
                if it.get("iter") == 0:
                    error = "N/A"
                else:
                    error = f"{error:.6f}%"

            row.append(error)
            self.tree.insert("", "end", values=row)

    def update_fields(self, method):
        if method == "Gauss con pivoteo parcial":
            self.x0_label.grid_remove()
            self.x0_entry.grid_remove()
            self.tol_label.grid_remove()
            self.tol_entry.grid_remove()
        else:
            self.x0_label.grid()
            self.x0_entry.grid()
            self.tol_label.grid()
            self.tol_entry.grid()

    def calculate(self):
        try:
            method = self.method_option.get()
            A = self.parse_matrix()
            n = len(A)
            b = self.parse_vector(self.vector_entry.get(), n, "vector b")

            if method == "Gauss con pivoteo parcial":
                result = gauss_pivoteo_parcial(A, b)

                summary = []
                summary.append("=== GAUSS CON PIVOTEO PARCIAL ===\n")

                sep = "-" * 34

                if isinstance(result, dict):
                    solution = result.get("solution")
                    summary.append("")
                    summary.append("DATOS DE ENTRADA")
                    summary.append(sep)
                    summary.append(f"Dimensión: {n} x {n}")
                    summary.append(f"Estado:    {result.get('message', 'Sin mensaje')}")
                    if solution is not None:
                        summary.append("")
                        summary.append("SOLUCIÓN FINAL")
                        summary.append(sep)
                        for i, val in enumerate(solution, start=1):
                            summary.append(f"x{i} = {val:12.6f}")

                        # Verificación: residuo Ax - b
                        residual = np.dot(np.array(A, dtype=float), np.array(solution)) - np.array(b, dtype=float)
                        summary.append("")
                        summary.append("VERIFICACIÓN (Ax - b)")
                        summary.append(sep)
                        summary.append(f"Residuo máximo: {np.max(np.abs(residual)):.6e}")
                        summary.append(f"Norma residuo:  {np.linalg.norm(residual):.6e}")
                        summary.append("Valores cercanos a cero confirman")
                        summary.append("la solución obtenida.")
                        self.setup_solution_table(solution)
                    else:
                        self.clear_table()
                    if "steps" in result:
                        summary.append("")
                        summary.append("PASO A PASO DEL MÉTODO")
                        summary.append(sep)
                        summary.append(result["steps"])
                else:
                    solution = result
                    sol_str = "[" + ", ".join(f"{x:.6f}" for x in solution) + "]" if isinstance(solution, list) else str(solution)
                    summary.append(f"Solución: {sol_str}")
                    self.setup_solution_table(solution)

                self.write_result("\n".join(map(str, summary)))

            elif method == "Gauss-Seidel":
                x0_text = self.x0_entry.get().strip()
                x0 = None if x0_text == "" else self.parse_vector(x0_text, n, "vector inicial x0")
                tol = float(self.tol_entry.get())

                result = gauss_seidel(A, b, x0=x0, tol=tol, max_iter=150)

                summary = []
                summary.append("=== GAUSS-SEIDEL ===\n")

                sep = "-" * 34

                if isinstance(result, dict):
                    iterations = result.get("iterations", [])

                    summary.append("")
                    summary.append("DATOS DE ENTRADA")
                    summary.append(sep)
                    summary.append(f"Dimensión:  {n} x {n}")
                    summary.append(f"x0:         {x0 if x0 is not None else 'vector de ceros'}")
                    summary.append(f"Tolerancia: {tol:g} %")
                    summary.append("Máx. iter.: 150")
                    summary.append("")

                    es_dominante, _ = check_diagonal_dominance(A)
                    summary.append("DIAGNÓSTICO")
                    summary.append(sep)
                    if es_dominante:
                        summary.append("Diagonal dominante estricta: Sí")
                        summary.append("La convergencia está garantizada.")
                    else:
                        summary.append("Diagonal dominante estricta: No")
                        summary.append("El método podría diverger o")
                        summary.append("converger lentamente.")
                    summary.append("")

                    summary.append("RESULTADOS")
                    summary.append(sep)
                    summary.append(f"Estado:      {result.get('message', 'Sin mensaje')}")
                    summary.append(f"Convergió:   {'Sí' if result.get('success') else 'No'}")
                    summary.append(f"Iteraciones: {len(iterations) - 1}")

                    if len(iterations) > 1 and isinstance(iterations[-1].get("error"), (int, float)):
                        summary.append(f"Error final: {iterations[-1]['error']:.6e} %")

                    sol = result.get('solution')
                    if isinstance(sol, list):
                        summary.append("")
                        summary.append("SOLUCIÓN APROXIMADA")
                        summary.append(sep)
                        for i, val in enumerate(sol, start=1):
                            summary.append(f"x{i} = {val:12.6f}")

                        # Verificación: residuo Ax - b
                        residual = np.dot(np.array(A, dtype=float), np.array(sol)) - np.array(b, dtype=float)
                        summary.append("")
                        summary.append("VERIFICACIÓN (Ax - b)")
                        summary.append(sep)
                        summary.append(f"Residuo máximo: {np.max(np.abs(residual)):.6e}")
                        summary.append(f"Norma residuo:  {np.linalg.norm(residual):.6e}")
                    else:
                        summary.append("Solución aproximada: N/A")

                    self.setup_iterations_table(iterations)
                else:
                    summary.append(f"Resultado: {result}")
                    self.clear_table()

                self.write_result("\n".join(map(str, summary)))

        except NotImplementedError:
            self.write_result(
                "El método todavía no está integrado.\n\n"
                "Pídele al compañero de sistemas que devuelva algo así:\n\n"
                "Para Gauss con pivoteo:\n"
                "{\n"
                '  "success": True,\n'
                '  "message": "Sistema resuelto correctamente",\n'
                '  "solution": [x1, x2, x3]\n'
                "}\n\n"
                "Para Gauss-Seidel:\n"
                "{\n"
                '  "success": True,\n'
                '  "message": "Convergió por tolerancia",\n'
                '  "solution": [x1, x2, x3],\n'
                '  "iterations": [\n'
                '      {"iter": 1, "x": [..], "error": 0.1},\n'
                '      {"iter": 2, "x": [..], "error": 0.01}\n'
                "  ]\n"
                "}"
            )
        except Exception as e:
            self.write_result(f"Error al calcular:\n{e}")

    def clear_fields(self):
        self.matrix_box.delete("1.0", "end")
        self.vector_entry.delete(0, "end")
        self.x0_entry.delete(0, "end")
        self.tol_entry.delete(0, "end")
        self.tol_entry.insert(0, "1e-6")
        self.method_option.set("Gauss con pivoteo parcial")
        self.update_fields("Gauss con pivoteo parcial")
        self.write_result("Aquí aparecerá el resumen del método.\n")
        self.clear_table()

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