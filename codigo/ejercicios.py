import numpy as np
from core.ui import titulo_principal, subtitulo, pedir_opcion, mensaje_info, mensaje_ok, pausa
from codigo.biseccion import biseccion
from codigo.newton_raices import newton
from codigo.secante import secante

def run_ejercicio_7(plot_evolution=False):
    subtitulo("EJERCICIO 7 - METODO DE BISECCION (Tolerancia: 1e-5)")
    
    # 7.a
    print("\n>>> Ejercicio 7.a: x - 2**(-x) = 0 en [0, 1]")
    fa = lambda x: x - 2.0**(-x)
    res_a = biseccion(fa, 0.0, 1.0, tol=1e-5, plot_evolution=plot_evolution)
    
    # 7.b
    print("\n>>> Ejercicio 7.b: e**x - x**2 + 3*x - 2 = 0 en [0, 1]")
    fb = lambda x: np.exp(x) - x**2 + 3.0*x - 2.0
    res_b = biseccion(fb, 0.0, 1.0, tol=1e-5, plot_evolution=plot_evolution)
    
    # 7.c
    print("\n>>> Ejercicio 7.c (Intervalo 1): 2*x*cos(2*x) - (x + 1)**2 = 0 en [-3, -2]")
    fc = lambda x: 2.0*x*np.cos(2.0*x) - (x + 1.0)**2
    res_c1 = biseccion(fc, -3.0, -2.0, tol=1e-5, plot_evolution=plot_evolution)
    
    print("\n>>> Ejercicio 7.c (Intervalo 2): 2*x*cos(2*x) - (x + 1)**2 = 0 en [-1, 0]")
    res_c2 = biseccion(fc, -1.0, 0.0, tol=1e-5, plot_evolution=plot_evolution)
    
    # 7.d
    print("\n>>> Ejercicio 7.d (Intervalo 1): x*cos(x) - 2*x**2 + 3*x - 1 = 0 en [0.2, 0.3]")
    fd = lambda x: x*np.cos(x) - 2.0*x**2 + 3.0*x - 1.0
    res_d1 = biseccion(fd, 0.2, 0.3, tol=1e-5, plot_evolution=plot_evolution)
    
    print("\n>>> Ejercicio 7.d (Intervalo 2): x*cos(x) - 2*x**2 + 3*x - 1 = 0 en [1.2, 1.3]")
    res_d2 = biseccion(fd, 1.2, 1.3, tol=1e-5, plot_evolution=plot_evolution)
    
    # Mostrar tabla resumen de Ejercicio 7
    print("\n" + "="*80)
    print("RESUMEN DE RESULTADOS - EJERCICIO 7 (BISECCIÓN)")
    print("="*80)
    print(f"{'Problema':<25} | {'Intervalo':<15} | {'Iteraciones':<12} | {'Raíz':<15} | {'f(Raíz)':<10}")
    print("-"*80)
    print(f"{'7.a':<25} | {'[0, 1]':<15} | {res_a['iteraciones']:<12} | {res_a['raiz']:<15.8f} | {res_a['f_raiz']:<10.2e}")
    print(f"{'7.b':<25} | {'[0, 1]':<15} | {res_b['iteraciones']:<12} | {res_b['raiz']:<15.8f} | {res_b['f_raiz']:<10.2e}")
    print(f"{'7.c (Intervalo 1)':<25} | {'[-3, -2]':<15} | {res_c1['iteraciones']:<12} | {res_c1['raiz']:<15.8f} | {res_c1['f_raiz']:<10.2e}")
    print(f"{'7.c (Intervalo 2)':<25} | {'[-1, 0]':<15} | {res_c2['iteraciones']:<12} | {res_c2['raiz']:<15.8f} | {res_c2['f_raiz']:<10.2e}")
    print(f"{'7.d (Intervalo 1)':<25} | {'[0.2, 0.3]':<15} | {res_d1['iteraciones']:<12} | {res_d1['raiz']:<15.8f} | {res_d1['f_raiz']:<10.2e}")
    print(f"{'7.d (Intervalo 2)':<25} | {'[1.2, 1.3]':<15} | {res_d2['iteraciones']:<12} | {res_d2['raiz']:<15.8f} | {res_d2['f_raiz']:<10.2e}")
    print("="*80 + "\n")

def run_abrevadero(plot_evolution=False):
    subtitulo("PROBLEMA DEL ABREVADERO - BISECCIÓN (Tolerancia: 1e-5)")
    
    # Ecuación del volumen
    # V = L * [0.5*pi*r**2 - r**2*arcsin(h/r) - h*sqrt(r**2 - h**2)]
    # L = 10, r = 1, V = 12.4
    # 12.4 = 10 * [0.5*pi - arcsin(h) - h*sqrt(1 - h**2)]
    # f(h) = 5*pi - 10*arcsin(h) - 10*h*sqrt(1 - h**2) - 12.4
    
    fh = lambda h: 5.0*np.pi - 10.0*np.arcsin(h) - 10.0*h*np.sqrt(1.0 - h**2) - 12.4
    
    print("Ecuación: f(h) = 5*pi - 10*arcsin(h) - 10*h*sqrt(1 - h**2) - 12.4 = 0")
    print("Intervalo de búsqueda: h en [0, 1] (0 = lleno, 1 = vacío)")
    
    res = biseccion(fh, 0.0, 1.0, tol=1e-5, plot_evolution=plot_evolution)
    
    h_sol = res["raiz"]
    profundidad_agua = 1.0 - h_sol
    
    print("="*80)
    print("RESULTADOS FINALES - PROBLEMA DEL ABREVADERO")
    print("="*80)
    print(f"Distancia h desde la parte superior: {h_sol:.8f} pies")
    print(f"Profundidad real del agua (r - h):   {profundidad_agua:.8f} pies")
    print(f"Volumen de agua calculado con h:     {10.0 * (0.5*np.pi - np.arcsin(h_sol) - h_sol*np.sqrt(1.0 - h_sol**2)):.6f} pies^3 (Esperado: 12.4)")
    print(f"Iteraciones realizadas:               {res['iteraciones']}")
    print(f"Convergencia:                         {res['mensaje']}")
    print("="*80 + "\n")

def run_ejercicio_6(plot_evolution=False):
    subtitulo("EJERCICIO 6 - METODOS DE NEWTON Y SECANTE (Tolerancia: 1e-5)")
    
    # 6.a: e**x + 2**(-x) + 2*cos(x) - 6 = 0 en [1, 2]
    # f'(x) = e**x - 2**(-x)*ln(2) - 2*sin(x)
    fa = lambda x: np.exp(x) + 2.0**(-x) + 2.0*np.cos(x) - 6.0
    dfa = lambda x: np.exp(x) - (2.0**(-x)) * np.log(2.0) - 2.0*np.sin(x)
    
    print("\n>>> Ejercicio 6.a: e**x + 2**(-x) + 2*cos(x) - 6 = 0")
    print("Ejecutando Newton (x0 = 1.5)...")
    res_a_n = newton(fa, dfa, 1.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(1.0, 2.0))
    print("Ejecutando Secante (x0 = 1.0, x1 = 2.0)...")
    res_a_s = secante(fa, 1.0, 2.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(1.0, 2.0))
    
    # 6.b: ln(x - 1) + cos(x - 1) = 0 en [1.3, 2]
    # f'(x) = 1/(x-1) - sin(x-1)
    fb = lambda x: np.log(x - 1.0) + np.cos(x - 1.0)
    dfb = lambda x: 1.0/(x - 1.0) - np.sin(x - 1.0)
    
    print("\n>>> Ejercicio 6.b: ln(x - 1) + cos(x - 1) = 0")
    print("Ejecutando Newton (x0 = 1.5)...")
    res_b_n = newton(fb, dfb, 1.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(1.3, 2.0))
    print("Ejecutando Secante (x0 = 1.3, x1 = 2.0)...")
    res_b_s = secante(fb, 1.3, 2.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(1.3, 2.0))
    
    # 6.c: 2*x*cos(2*x) - (x - 2)**2 = 0
    # f'(x) = 2*cos(2*x) - 4*x*sin(2*x) - 2*(x - 2)
    fc = lambda x: 2.0*x*np.cos(2.0*x) - (x - 2.0)**2
    dfc = lambda x: 2.0*np.cos(2.0*x) - 4.0*x*np.sin(2.0*x) - 2.0*(x - 2.0)
    
    print("\n>>> Ejercicio 6.c (Intervalo 1): 2*x*cos(2*x) - (x - 2)**2 = 0 en [2, 3]")
    print("Ejecutando Newton (x0 = 2.5)...")
    res_c1_n = newton(fc, dfc, 2.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(2.0, 3.0))
    print("Ejecutando Secante (x0 = 2.0, x1 = 3.0)...")
    res_c1_s = secante(fc, 2.0, 3.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(2.0, 3.0))
    
    print("\n>>> Ejercicio 6.c (Intervalo 2): 2*x*cos(2*x) - (x - 2)**2 = 0 en [3, 4]")
    print("Ejecutando Newton (x0 = 3.5)...")
    res_c2_n = newton(fc, dfc, 3.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(3.0, 4.0))
    print("Ejecutando Secante (x0 = 3.0, x1 = 4.0)...")
    res_c2_s = secante(fc, 3.0, 4.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(3.0, 4.0))
    
    # 6.d: (x - 2)**2 - ln(x) = 0
    # f'(x) = 2*(x - 2) - 1/x
    fd = lambda x: (x - 2.0)**2 - np.log(x)
    dfd = lambda x: 2.0*(x - 2.0) - 1.0/x
    
    print("\n>>> Ejercicio 6.d (Intervalo 1): (x - 2)**2 - ln(x) = 0 en [1, 2]")
    print("Ejecutando Newton (x0 = 1.5)...")
    res_d1_n = newton(fd, dfd, 1.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(1.0, 2.0))
    print("Ejecutando Secante (x0 = 1.0, x1 = 2.0)...")
    res_d1_s = secante(fd, 1.0, 2.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(1.0, 2.0))
    
    print("\n>>> Ejercicio 6.d (Intervalo 2): (x - 2)**2 - ln(x) = 0 en [e, 4]")
    print("Ejecutando Newton (x0 = 3.0)...")
    res_d2_n = newton(fd, dfd, 3.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(np.e, 4.0))
    print("Ejecutando Secante (x0 = e, x1 = 4.0)...")
    res_d2_s = secante(fd, np.e, 4.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(np.e, 4.0))
    
    # 6.e: e**x - 3*x**2 = 0
    # f'(x) = e**x - 6*x
    fe = lambda x: np.exp(x) - 3.0*x**2
    dfe = lambda x: np.exp(x) - 6.0*x
    
    print("\n>>> Ejercicio 6.e (Intervalo 1): e**x - 3*x**2 = 0 en [0, 1]")
    print("Ejecutando Newton (x0 = 0.5)...")
    res_e1_n = newton(fe, dfe, 0.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(0.0, 1.0))
    print("Ejecutando Secante (x0 = 0.0, x1 = 1.0)...")
    res_e1_s = secante(fe, 0.0, 1.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(0.0, 1.0))
    
    print("\n>>> Ejercicio 6.e (Intervalo 2): e**x - 3*x**2 = 0 en [3, 5]")
    print("Ejecutando Newton (x0 = 4.0)...")
    res_e2_n = newton(fe, dfe, 4.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(3.0, 5.0))
    print("Ejecutando Secante (x0 = 3.0, x1 = 5.0)...")
    res_e2_s = secante(fe, 3.0, 5.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(3.0, 5.0))
    
    # 6.f: sen(x) - e**(-x) = 0
    # f'(x) = cos(x) + e**(-x)
    ff = lambda x: np.sin(x) - np.exp(-x)
    dff = lambda x: np.cos(x) + np.exp(-x)
    
    print("\n>>> Ejercicio 6.f (Intervalo 1): sen(x) - e**(-x) = 0 en [0, 1]")
    print("Ejecutando Newton (x0 = 0.5)...")
    res_f1_n = newton(ff, dff, 0.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(0.0, 1.0))
    print("Ejecutando Secante (x0 = 0.0, x1 = 1.0)...")
    res_f1_s = secante(ff, 0.0, 1.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(0.0, 1.0))
    
    print("\n>>> Ejercicio 6.f (Intervalo 2): sen(x) - e**(-x) = 0 en [3, 4]")
    print("Ejecutando Newton (x0 = 3.5)...")
    res_f2_n = newton(ff, dff, 3.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(3.0, 4.0))
    print("Ejecutando Secante (x0 = 3.0, x1 = 4.0)...")
    res_f2_s = secante(ff, 3.0, 4.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(3.0, 4.0))
    
    print("\n>>> Ejercicio 6.f (Intervalo 3): sen(x) - e**(-x) = 0 en [6, 7]")
    print("Ejecutando Newton (x0 = 6.5)...")
    res_f3_n = newton(ff, dff, 6.5, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(6.0, 7.0))
    print("Ejecutando Secante (x0 = 6.0, x1 = 7.0)...")
    res_f3_s = secante(ff, 6.0, 7.0, tol=1e-5, plot_evolution=plot_evolution, domain_grafico=(6.0, 7.0))
    
    # Tabla comparativa de resultados Ejercicio 6
    print("\n" + "="*100)
    print("TABLA COMPARATIVA - EJERCICIO 6 (NEWTON vs SECANTE)")
    print("="*100)
    print(f"{'Problema':<22} | {'Método':<10} | {'Iteraciones':<12} | {'Raíz Encontrada':<18} | {'f(Raíz)':<10}")
    print("-"*100)
    
    # 6.a
    print(f"{'6.a en [1, 2]':<22} | {'Newton':<10} | {res_a_n['iteraciones']:<12} | {res_a_n['raiz']:<18.10f} | {res_a_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_a_s['iteraciones']:<12} | {res_a_s['raiz']:<18.10f} | {res_a_s['f_raiz']:<10.2e}")
    print("-"*100)
    
    # 6.b
    print(f"{'6.b en [1.3, 2]':<22} | {'Newton':<10} | {res_b_n['iteraciones']:<12} | {res_b_n['raiz']:<18.10f} | {res_b_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_b_s['iteraciones']:<12} | {res_b_s['raiz']:<18.10f} | {res_b_s['f_raiz']:<10.2e}")
    print("-"*100)
    
    # 6.c
    print(f"{'6.c en [2, 3]':<22} | {'Newton':<10} | {res_c1_n['iteraciones']:<12} | {res_c1_n['raiz']:<18.10f} | {res_c1_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_c1_s['iteraciones']:<12} | {res_c1_s['raiz']:<18.10f} | {res_c1_s['f_raiz']:<10.2e}")
    print(f"{'6.c en [3, 4]':<22} | {'Newton':<10} | {res_c2_n['iteraciones']:<12} | {res_c2_n['raiz']:<18.10f} | {res_c2_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_c2_s['iteraciones']:<12} | {res_c2_s['raiz']:<18.10f} | {res_c2_s['f_raiz']:<10.2e}")
    print("-"*100)
    
    # 6.d
    print(f"{'6.d en [1, 2]':<22} | {'Newton':<10} | {res_d1_n['iteraciones']:<12} | {res_d1_n['raiz']:<18.10f} | {res_d1_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_d1_s['iteraciones']:<12} | {res_d1_s['raiz']:<18.10f} | {res_d1_s['f_raiz']:<10.2e}")
    print(f"{'6.d en [e, 4]':<22} | {'Newton':<10} | {res_d2_n['iteraciones']:<12} | {res_d2_n['raiz']:<18.10f} | {res_d2_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_d2_s['iteraciones']:<12} | {res_d2_s['raiz']:<18.10f} | {res_d2_s['f_raiz']:<10.2e}")
    print("-"*100)
    
    # 6.e
    print(f"{'6.e en [0, 1]':<22} | {'Newton':<10} | {res_e1_n['iteraciones']:<12} | {res_e1_n['raiz']:<18.10f} | {res_e1_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_e1_s['iteraciones']:<12} | {res_e1_s['raiz']:<18.10f} | {res_e1_s['f_raiz']:<10.2e}")
    print(f"{'6.e en [3, 5]':<22} | {'Newton':<10} | {res_e2_n['iteraciones']:<12} | {res_e2_n['raiz']:<18.10f} | {res_e2_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_e2_s['iteraciones']:<12} | {res_e2_s['raiz']:<18.10f} | {res_e2_s['f_raiz']:<10.2e}")
    print("-"*100)
    
    # 6.f
    print(f"{'6.f en [0, 1]':<22} | {'Newton':<10} | {res_f1_n['iteraciones']:<12} | {res_f1_n['raiz']:<18.10f} | {res_f1_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_f1_s['iteraciones']:<12} | {res_f1_s['raiz']:<18.10f} | {res_f1_s['f_raiz']:<10.2e}")
    print(f"{'6.f en [3, 4]':<22} | {'Newton':<10} | {res_f2_n['iteraciones']:<12} | {res_f2_n['raiz']:<18.10f} | {res_f2_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_f2_s['iteraciones']:<12} | {res_f2_s['raiz']:<18.10f} | {res_f2_s['f_raiz']:<10.2e}")
    print(f"{'6.f en [6, 7]':<22} | {'Newton':<10} | {res_f3_n['iteraciones']:<12} | {res_f3_n['raiz']:<18.10f} | {res_f3_n['f_raiz']:<10.2e}")
    print(f"{'':<22} | {'Secante':<10} | {res_f3_s['iteraciones']:<12} | {res_f3_s['raiz']:<18.10f} | {res_f3_s['f_raiz']:<10.2e}")
    print("="*100 + "\n")

def menu_ejercicios_predefinidos():
    while True:
        titulo_principal("EJERCICIOS PREDEFINIDOS Y CASOS DE PRUEBA")
        print("1. Ejercicio 7 (Bisección: a, b, c, d)")
        print("2. Problema del Abrevadero (Bisección)")
        print("3. Ejercicio 6 (Newton y Secante: a, b, c, d, e, f)")
        print("4. Ejecutar TODOS los Ejercicios de una vez")
        print("0. Volver")
        
        opcion = pedir_opcion("\nSeleccione una opción: ", ["1", "2", "3", "4", "0"])
        
        if opcion == "0":
            break
            
        # Preguntar si desea graficación
        graf_opc = pedir_opcion("¿Desea activar la graficación interactiva paso a paso? (s/n): ", ["s", "n"])
        plot_evolution = (graf_opc == "s")
        
        if opcion == "1":
            try:
                run_ejercicio_7(plot_evolution=plot_evolution)
            except Exception as e:
                print(f"[ERROR] Ocurrió un error en el Ejercicio 7: {e}")
            pausa()
            
        elif opcion == "2":
            try:
                run_abrevadero(plot_evolution=plot_evolution)
            except Exception as e:
                print(f"[ERROR] Ocurrió un error en el Abrevadero: {e}")
            pausa()
            
        elif opcion == "3":
            try:
                run_ejercicio_6(plot_evolution=plot_evolution)
            except Exception as e:
                print(f"[ERROR] Ocurrió un error en el Ejercicio 6: {e}")
            pausa()
            
        elif opcion == "4":
            try:
                mensaje_info("Ejecutando Ejercicio 7...")
                run_ejercicio_7(plot_evolution=plot_evolution)
                mensaje_info("Ejecutando Problema del Abrevadero...")
                run_abrevadero(plot_evolution=plot_evolution)
                mensaje_info("Ejecutando Ejercicio 6...")
                run_ejercicio_6(plot_evolution=plot_evolution)
                mensaje_ok("Todos los ejercicios completados con éxito.")
            except Exception as e:
                print(f"[ERROR] Ocurrió un error general: {e}")
            pausa()
