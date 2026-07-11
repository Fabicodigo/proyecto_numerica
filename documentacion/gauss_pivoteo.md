# Eliminación Gaussiana con Pivoteo Parcial

Documento explicativo del script [`gauss_pivoteo.py`](../codigo/gauss_pivoteo.py).
Implementa el algoritmo de eliminación con pivoteo parcial detallado en la **Parte 3** de Chapra & Canale, *Métodos numéricos para ingenieros*.

---

## 1. ¿Qué problema resuelve?

Resuelve un sistema de ecuaciones algebraicas lineales de la forma:
$$Ax = b$$

Donde $A$ es la matriz cuadrada de coeficientes de tamaño $n \times n$, $b$ es el vector de términos independientes de tamaño $n$, y $x$ es el vector de incógnitas a resolver.

---

## 2. La fórmula y el algoritmo

El método consta de dos fases principales:

### a) Eliminación hacia adelante (Triangulación)
Transforma la matriz original $A$ en una matriz triangular superior, modificando simultáneamente el vector $b$. Para cada columna $k$:
1. **Pivoteo Parcial:** Se busca en la columna $k$ (desde la fila $k$ hasta la última) el elemento con el valor absoluto máximo. Si está en otra fila $p$, se intercambia la fila $k$ con la fila $p$ en la matriz aumentada $[A|b]$.
2. **Eliminación:** Para cada fila $i$ debajo del pivote ($i > k$), se calcula el factor:
   $$m_{i,k} = \frac{A_{i,k}}{A_{k,k}}$$
   Y se realiza la operación sobre la fila $i$:
   $$\text{Fila}_i = \text{Fila}_i - m_{i,k} \cdot \text{Fila}_k$$

### b) Sustitución hacia atrás
Resuelve de manera directa las incógnitas empezando por la última variable ($x_n$) hasta la primera ($x_1$):
$$x_n = \frac{b_n}{A_{n,n}}$$
$$x_i = \frac{b_i - \sum_{j=i+1}^{n} A_{i,j} \cdot x_j}{A_{i,i}} \quad \text{para } i = n-1, n-2, \dots, 1$$

---

## 3. ¿Por qué es necesario el Pivoteo Parcial?

Si un elemento en la diagonal principal $A_{k,k}$ es cero o muy cercano a cero, el multiplicador $m_{i,k}$ tiende a infinito. Esto causa:
1. **Fallo por división entre cero:** El programa se interrumpe inmediatamente.
2. **Errores por redondeo:** Los valores numéricos enormes amplifican la imprecisión del punto flotante, arruinando la solución.

El pivoteo parcial por máximo de columna soluciona ambos problemas al garantizar que el pivote de turno siempre sea el elemento con mayor magnitud absoluta disponible en esa columna.

---

## 4. Recorrido del código, bloque por bloque

### 4.1 Búsqueda de pivote e intercambio
```python
pivot_row = k + np.argmax(np.abs(M[k:, k]))
max_val = np.abs(M[pivot_row, k])

if max_val < 1e-12:
    raise ValueError(f"Error: La columna {k+1} tiene solo ceros en su diagonal inferior. Matriz singular.")

if pivot_row != k:
    M[[k, pivot_row]] = M[[pivot_row, k]]
```
Usa `np.argmax` sobre los valores absolutos inferiores de la columna para hallar la fila con el coeficiente mayor e intercambiarla físicamente mediante indexación avanzada de NumPy.

### 4.2 Eliminación en la columna
```python
pivot = M[k, k]
for i in range(k + 1, n):
    factor = M[i, k] / pivot
    M[i, k:] -= factor * M[k, k:]
```
Calcula los factores y realiza la resta de filas de forma vectorizada sobre toda la porción restante de la matriz aumentada.

### 4.3 Sustitución hacia atrás
```python
x = np.zeros(n)
x[n-1] = M[n-1, n] / M[n-1, n-1]

for i in range(n - 2, -1, -1):
    sum_terms = np.dot(M[i, i+1:n], x[i+1:n])
    x[i] = (M[i, n] - sum_terms) / M[i, i]
```
Calcula la última incógnita y usa `np.dot` para obtener de forma eficiente la suma de los términos conocidos y resolver hacia atrás las incógnitas restantes.

---

## 5. Ejemplo de verificación (Chapra 12.1)

Para resolver el sistema de balance de masa en reactores acoplados en estado estacionario:
* Matriz de coeficientes $A$ y vector $b$:
```text
A = [[15, -3, -1],
     [-3, 18, -6],
     [-4, -1, 12]]
b = [2400, 0, 0]
```

La salida del programa es:
```text
Solucion final calculada:
x_1 = 180.3478
x_2 = 47.9130
x_3 = 64.1043
```
Coincide con los cálculos exactos presentados en el libro de Chapra.

---

## 6. Cómo ejecutarlo

### Ejecución directa en terminal
Puedes probar el funcionamiento interactivo corriendo el script de consola general del proyecto:
```bash
python main.py
```
O ejecutando el entorno gráfico:
```bash
python app.py
```

### Usar las funciones desde otro script
```python
import numpy as np
from codigo.gauss_pivoteo import gauss_pivoteo_parcial

A = np.array([[4.0, 1.0], [2.0, 3.0]])
b = np.array([1.0, 2.0])

result = gauss_pivoteo_parcial(A, b)
print("Solución:", result["solution"])  # -> [0.100000, 0.600000]
```
