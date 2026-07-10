from config import LINE, DOUBLE_LINE

def limpiar():
    print("\n" * 2)

def titulo_principal(texto):
    print("\n" + DOUBLE_LINE)
    print(texto.center(60))
    print(DOUBLE_LINE)

def subtitulo(texto):
    print("\n" + LINE)
    print(texto)
    print(LINE)

def mensaje_info(texto):
    print(f"[INFO] {texto}")

def mensaje_ok(texto):
    print(f"[OK] {texto}")

def mensaje_error(texto):
    print(f"[ERROR] {texto}")

def pausa():
    input("\nPresione Enter para continuar...")

def pedir_opcion(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        mensaje_error(f"Opción inválida. Opciones válidas: {', '.join(opciones_validas)}")

def pedir_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            mensaje_error("Debe ingresar un número válido.")

def pedir_int(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            mensaje_error("Debe ingresar un número entero válido.")

def pedir_float_positivo(mensaje):
    while True:
        valor = pedir_float(mensaje)
        if valor > 0:
            return valor
        mensaje_error("El valor debe ser positivo.")

def pedir_int_positivo(mensaje):
    while True:
        valor = pedir_int(mensaje)
        if valor > 0:
            return valor
        mensaje_error("El valor debe ser un entero positivo.")

def pedir_lista_floats(mensaje):
    while True:
        try:
            valores = input(mensaje).strip().split()
            return [float(v) for v in valores]
        except ValueError:
            mensaje_error("Ingrese solo números separados por espacios.")

def pedir_puntos_xy():
    subtitulo("INGRESO DE DATOS DE INTERPOLACIÓN")
    x = pedir_lista_floats("Ingrese los valores de x separados por espacios: ")
    y = pedir_lista_floats("Ingrese los valores de y separados por espacios: ")

    if len(x) != len(y):
        mensaje_error("Las listas x e y deben tener la misma cantidad de elementos.")
        return None, None

    if len(x) < 2:
        mensaje_error("Debe ingresar al menos 2 puntos.")
        return None, None

    return x, y

def pedir_funcion_texto():
    subtitulo("INGRESO DE FUNCIÓN")
    return input("Ingrese la función f(x) usando la variable x: ").strip()

def pedir_intervalo():
    subtitulo("INGRESO DEL INTERVALO")
    a = pedir_float("Ingrese el extremo izquierdo a: ")
    b = pedir_float("Ingrese el extremo derecho b: ")
    return a, b

def pedir_matriz_vector():
    subtitulo("INGRESO DEL SISTEMA DE ECUACIONES")
    n = pedir_int_positivo("Ingrese el número de ecuaciones / incógnitas: ")

    A = []
    print("\nIngrese la matriz A fila por fila.")
    print("Ejemplo de fila: 2 -1 3")

    for i in range(n):
        while True:
            fila = pedir_lista_floats(f"Fila {i+1}: ")
            if len(fila) == n:
                A.append(fila)
                break
            mensaje_error(f"La fila debe tener exactamente {n} elementos.")

    while True:
        b = pedir_lista_floats(f"Ingrese el vector b con {n} elementos: ")
        if len(b) == n:
            break
        mensaje_error(f"El vector b debe tener exactamente {n} elementos.")

    return A, b

def pedir_vector_inicial(n):
    while True:
        x0 = pedir_lista_floats(f"Ingrese el vector inicial x0 con {n} elementos: ")
        if len(x0) == n:
            return x0
        mensaje_error(f"El vector inicial debe tener exactamente {n} elementos.")

def mostrar_resultado_escalar(titulo, valor, decimales=6):
    subtitulo(titulo)
    print(f"Resultado: {valor:.{decimales}f}")

def mostrar_resultado_texto(titulo, texto):
    subtitulo(titulo)
    print(texto)

def mostrar_resultado_newton_interpolacion(xi, yint, ea):
    subtitulo("RESULTADOS - INTERPOLACIÓN DE NEWTON")
    print(f"Valor interpolado en xi = {xi}: {yint[-1]:.6f}\n")

    print("Evolución por grado:")
    for i, valor in enumerate(yint):
        print(f"  Grado {i}: {valor:.6f}")

    print("\nErrores aproximados:")
    for i, err in enumerate(ea):
        print(f"  Error grado {i}: {err}")

def mostrar_matriz(A, nombre="Matriz"):
    subtitulo(nombre)
    for fila in A:
        print("  ", fila)