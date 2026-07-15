import customtkinter as ctk
from gui.integration_view import IntegrationView
from gui.systems_view import SystemsView
from gui.roots_view import RootsView
from gui.interpolation_view import InterpolationView
from gui.problems18_view import Problems18View

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Proyecto - Programación Numérica")
        self.geometry("1100x700")
        self.minsize(1000, 650)

        # Layout general
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(10, weight=1)

        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text="Programación\nNumérica",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_roots = ctk.CTkButton(
            self.sidebar, text="Métodos de raíces", command=self.show_roots
        )
        self.btn_roots.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_systems = ctk.CTkButton(
            self.sidebar, text="Sistemas lineales", command=self.show_systems
        )
        self.btn_systems.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_interpolation = ctk.CTkButton(
            self.sidebar, text="Interpolación", command=self.show_interpolation
        )
        self.btn_interpolation.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_integration = ctk.CTkButton(
            self.sidebar, text="Integración numérica", command=self.show_integration
        )
        self.btn_integration.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_problems18 = ctk.CTkButton(
            self.sidebar, text="Guía Cap. 18", command=self.show_problems18
        )
        self.btn_problems18.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.btn_exit = ctk.CTkButton(
            self.sidebar, text="Salir", fg_color="#c0392b", hover_color="#a93226",
            command=self.destroy
        )
        self.btn_exit.grid(row=11, column=0, padx=20, pady=30, sticky="ew")

        # Área principal
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.current_view = None
        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        title = ctk.CTkLabel(
            frame,
            text="Bienvenido al Proyecto de Programación Numérica",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(40, 20))

        subtitle = ctk.CTkLabel(
            frame,
            text="Seleccione un módulo en el panel izquierdo para comenzar.",
            font=ctk.CTkFont(size=18)
        )
        subtitle.pack(pady=10)

    def show_roots(self):
        self.clear_content()
        view = RootsView(self.content)
        view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_systems(self):
        self.clear_content()
        view = SystemsView(self.content)
        view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_interpolation(self):
        self.clear_content()
        view = InterpolationView(self.content)
        view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_integration(self):
        self.clear_content()
        view = IntegrationView(self.content)
        view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_problems18(self):
        self.clear_content()
        view = Problems18View(self.content)
        view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)