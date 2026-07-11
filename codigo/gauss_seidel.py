import numpy as np
from typing import Tuple, List

def check_diagonal_dominance(A: np.ndarray) -> Tuple[bool, List[str]]:
    """
    Comprueba si una matriz es estrictamente diagonal dominante.
    Retorna (es_dominante, razones_de_fallo).
    """
    A = np.array(A, dtype=float)
    n = len(A)
    is_sdd = True
    reasons = []
    
    for i in range(n):
        diag = abs(A[i, i])
        off_diag = np.sum(np.abs(A[i])) - diag
        if diag <= off_diag:
            is_sdd = False
            reasons.append(f"Fila {i+1}: |A_{i+1},{i+1}| = {diag:.4f} <= Suma Extradiagonal = {off_diag:.4f}")
            
    return is_sdd, reasons

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=150):
    """
    Resuelve el sistema Ax = b usando el metodo iterativo de Gauss-Seidel.
    Muestra la evaluacion de dominancia diagonal y retorna los pasos de chequeo.
    """
    A_arr = np.array(A, dtype=float)
    b_arr = np.array(b, dtype=float)
    
    # Validaciones de entrada
    if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
        raise ValueError("Error: La matriz A debe ser cuadrada (n x n).")
    if len(b_arr) != A_arr.shape[0]:
        raise ValueError("Error: El vector b debe tener la misma longitud que el número de filas de A.")
        
    n = len(A_arr)
    
    # Validar que no haya ceros en la diagonal principal
    for i in range(n):
        if abs(A_arr[i, i]) < 1e-12:
            raise ValueError(f"Error: El elemento en la diagonal A[{i+1},{i+1}] es cercano a cero. Gauss-Seidel no puede dividir por cero.")
            
    # Comprobar dominancia diagonal
    is_sdd, reasons = check_diagonal_dominance(A_arr)
    
    steps = []
    
    def log(msg):
        print(msg)
        steps.append(msg)
        
    log("=== INICIO: ITERACIÓN DE GAUSS-SEIDEL ===")
    log("Evaluando Dominancia Diagonal Estricta (DDE):")
    if is_sdd:
        log("[✓] La matriz es estrictamente diagonal dominante. Convergencia garantizada.\n")
    else:
        log("[!] ADVERTENCIA: La matriz NO es estrictamente diagonal dominante.")
        log("Detalles de filas no dominantes:")
        for r in reasons:
            log(f"  - {r}")
        log("El metodo podria divergir o converger muy lentamente. Se procedera bajo su riesgo.\n")
        
    # Inicializar estimacion inicial
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float)
        
    # Imprimir cabecera de la tabla de convergencia en consola
    headers = f"{'Iter':<5} | " + " | ".join(f"x_{i+1:<8}" for i in range(n)) + f" | {'Error Max (%)':<15}"
    print("-" * len(headers))
    print(headers)
    print("-" * len(headers))
    
    # Primera fila (inicial)
    x_str = " | ".join(f"{val:10.6f}" for val in x)
    print(f"{0:<5} | {x_str} | {'---':<15}")
    
    iterations_log = []
    # Log de iteracion inicial (0)
    iterations_log.append({
        "iter": 0,
        "x": x.tolist(),
        "error": 100.0
    })
    
    converged = False
    
    for k in range(1, max_iter + 1):
        x_old = x.copy()
        
        # Iteracion para cada variable
        for i in range(n):
            sum_new = np.dot(A_arr[i, :i], x[:i])
            sum_old = np.dot(A_arr[i, i+1:], x_old[i+1:])
            x[i] = (b_arr[i] - sum_new - sum_old) / A_arr[i, i]
            
        # Calcular errores aproximados relativos porcentuales
        errors = np.zeros(n)
        for i in range(n):
            if abs(x[i]) > 1e-12:
                errors[i] = abs((x[i] - x_old[i]) / x[i]) * 100
            else:
                errors[i] = 0.0
                
        max_err = np.max(errors)
        
        # Guardar en el log de iteraciones
        iterations_log.append({
            "iter": k,
            "x": x.tolist(),
            "error": float(max_err)
        })
        
        # Imprimir fila actual en consola
        x_str = " | ".join(f"{val:10.6f}" for val in x)
        print(f"{k:<5} | {x_str} | {max_err:13.6f}%")
        
        # Comprobar criterio de parada
        if max_err < tol:
            print("-" * len(headers))
            print(f"[✓] CONVERGENCIA ALCANZADA en la iteracion {k} con un error de {max_err:.8f}%.")
            converged = True
            break
            
    if not converged:
        print("-" * len(headers))
        print(f"[!] LIMITE DE ITERACIONES ALCANZADO ({max_iter} iteraciones) sin alcanzar la tolerancia requerida.")
        
    # Calcular residuo final
    residual = np.dot(A_arr, x) - b_arr
    residual_norm = np.linalg.norm(residual)
    print(f"Norma del residuo final ||Ax - b||: {residual_norm:.8f}")
    print("=========================================\n")
    
    log(f"Norma del residuo final ||Ax - b||: {residual_norm:.8e}")
    
    return {
        "success": converged,
        "message": f"Convergió en {k} iteraciones" if converged else "Límite de iteraciones alcanzado sin convergencia",
        "solution": x.tolist(),
        "iterations": iterations_log,
        "steps": "\n".join(steps)
    }
