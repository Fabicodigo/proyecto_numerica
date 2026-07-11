import numpy as np

def gauss_pivoteo_parcial(A, b):
    """
    Resuelve el sistema Ax = b usando Eliminacion Gaussiana con
    pivoteo parcial por maximo de columna.
    Retorna un diccionario con la solucion y el paso a paso detallado.
    """
    # Convertir a flotantes de numpy
    A_arr = np.array(A, dtype=float)
    b_arr = np.array(b, dtype=float)
    
    # Validaciones de entrada
    if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
        raise ValueError("Error: La matriz A debe ser cuadrada (n x n).")
    if len(b_arr) != A_arr.shape[0]:
        raise ValueError("Error: El vector b debe tener la misma longitud que el número de filas de A.")
        
    n = len(A_arr)
    
    # Crear matriz aumentada M = [A | b]
    M = np.hstack([A_arr, b_arr.reshape(-1, 1)])
    
    steps = []
    
    def log(msg):
        print(msg)
        steps.append(msg)
        
    def log_matrix(Mat):
        for i in range(n):
            row_str = "  ".join(f"{val:10.4f}" for val in Mat[i, :-1])
            log(f"[ {row_str}  |  {Mat[i, -1]:10.4f} ]")
        log("")

    log("=== INICIO: ELIMINACIÓN GAUSSIANA CON PIVOTEO ===")
    log("Matriz aumentada inicial [A | b]:")
    log_matrix(M)
    
    # Fase de eliminacion hacia adelante
    for k in range(n):
        log(f"--- ETAPA DE ELIMINACIÓN K = {k+1} ---")
        
        # 1. Buscar fila pivote en la columna k
        pivot_row = k + np.argmax(np.abs(M[k:, k]))
        max_val = np.abs(M[pivot_row, k])
        
        # Validar si el pivote es cercano a cero (singularidad)
        if max_val < 1e-12:
            raise ValueError(f"Error: La columna {k+1} tiene solo ceros en su diagonal inferior. Matriz singular.")
        
        # 2. Intercambiar filas si es necesario
        if pivot_row != k:
            M[[k, pivot_row]] = M[[pivot_row, k]]
            log(f"-> PIVOTEO: Intercambio Fila {k+1} con Fila {pivot_row+1}")
            log("Matriz despues del intercambio:")
            log_matrix(M)
        else:
            log(f"-> PIVOTEO: No se requiere intercambio (Fila {k+1} tiene el maximo absoluto: {M[k, k]:.4f})")
            
        pivot = M[k, k]
        
        # 3. Eliminar elementos bajo el pivote
        for i in range(k + 1, n):
            factor = M[i, k] / pivot
            M[i, k:] -= factor * M[k, k:]
            log(f"  Fila {i+1} = Fila {i+1} - ({factor:.6f}) * Fila {k+1}")
            
        log("\nMatriz despues de la eliminacion en columna:")
        log_matrix(M)
        
    # Fase de sustitucion hacia atras
    x = np.zeros(n)
    log("--- SUSTITUCIÓN HACIA ATRÁS ---")
    x[n-1] = M[n-1, n] / M[n-1, n-1]
    log(f"x[{n}] = {M[n-1, n]:.6f} / {M[n-1, n-1]:.6f} = {x[n-1]:.6f}")
    
    for i in range(n - 2, -1, -1):
        sum_terms = np.dot(M[i, i+1:n], x[i+1:n])
        x[i] = (M[i, n] - sum_terms) / M[i, i]
        log(f"x[{i+1}] = ({M[i, n]:.6f} - {sum_terms:.6f}) / {M[i, i]:.6f} = {x[i]:.6f}")
        
    log("\nSolucion final calculada:")
    for idx, val in enumerate(x):
        log(f"x_{idx+1} = {val:.6f}")
    log("=================================================\n")
    
    return {
        "success": True,
        "message": "Sistema resuelto correctamente",
        "solution": x.tolist(),
        "steps": "\n".join(steps)
    }