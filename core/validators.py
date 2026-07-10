def validar_puntos_xy(x, y):
    if len(x) != len(y):
        return False, "Las listas x e y deben tener la misma cantidad de elementos."
    if len(x) == 0:
        return False, "Las listas no pueden estar vacías."
    return True, ""

def validar_intervalo(a, b):
    if a >= b:
        return False, "El extremo izquierdo debe ser menor que el derecho."
    return True, ""

def validar_matriz(A, b):
    if len(A) == 0:
        return False, "La matriz no puede estar vacía."
    filas = len(A)
    columnas = len(A[0])

    for fila in A:
        if len(fila) != columnas:
            return False, "Todas las filas de la matriz deben tener la misma longitud."

    if len(b) != filas:
        return False, "El vector b debe tener la misma cantidad de filas que A."

    return True, ""