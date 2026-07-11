# Método Iterativo de Gauss-Seidel

Documento explicativo del script [`gauss_seidel.py`](../codigo/gauss_seidel.py).
Implementa el algoritmo iterativo con criterio de convergencia del **Capítulo 11** de Chapra & Canale, *Métodos numéricos para ingenieros*.

---

## 1. ¿Qué problema resuelve?

Al igual que la eliminación gaussiana, resuelve el sistema lineal:
$$Ax = b$$

La diferencia principal es que es un **método iterativo**. En lugar de resolver el sistema de forma directa mediante operaciones de fila, parte de una estimación inicial de soluciones $x^{(0)}$ (típicamente ceros) y genera sucesivamente mejores aproximaciones hasta alcanzar la precisión (tolerancia) deseada.

---

## 2. La fórmula

La ecuación de recurrencia para cada variable $x_i$ en la iteración $k+1$ es:
$$x_i^{(k+1)} = \frac{b_i - \sum_{j < i} A_{i,j} x_j^{(k+1)} - \sum_{j > i} A_{i,j} x_j^{(k)}}{A_{i,i}}$$

### Característica Clave (vs Jacobi):
En Gauss-Seidel, tan pronto como se calcula un nuevo valor para una variable $x_i$ dentro de la iteración actual, este se utiliza **inmediatamente** para calcular las siguientes variables de la misma iteración. Esto acelera notablemente la convergencia.

---

## 3. Criterio de Convergencia: Dominancia Diagonal Estricta (DDE)

El método converge garantizadamente desde cualquier vector inicial si la matriz $A$ es **estrictamente diagonal dominante (DDE)**:
$$|A_{i,i}| > \sum_{j \neq i} |A_{i,j}| \quad \forall i = 1, 2, \dots, n$$

### Análisis de nuestro caso de estudio:
Para los reactores acoplados en los problemas 12.1 y 12.4, la matriz es **débilmente diagonal dominante** (en algunas filas, el término diagonal es igual a la suma de los extradiagonales, no estrictamente mayor).
* A pesar de esto, el método converge porque el radio espectral de su matriz de iteración es estrictamente menor que 1 ($\rho(T_{GS}) < 1$).
* El código evalúa y alerta esta situación antes de iniciar las iteraciones.

---

## 4. Recorrido del código, bloque por bloque

### 4.1 Evaluación de dominancia diagonal
```python
is_sdd = True
reasons = []
for i in range(n):
    diag = abs(A[i, i])
    off_diag = np.sum(np.abs(A[i])) - diag
    if diag <= off_diag:
        is_sdd = False
        reasons.append(f"Fila {i+1}: |A_{i+1},{i+1}| = {diag:.4f} <= Suma Extradiagonal = {off_diag:.4f}")
```
Analiza fila por fila si el elemento diagonal supera estrictamente a la suma absoluta de los elementos de su misma fila.

### 4.2 Iteración del método y actualización inmediata
```python
for i in range(n):
    sum_new = np.dot(A_arr[i, :i], x[:i])
    sum_old = np.dot(A_arr[i, i+1:], x_old[i+1:])
    x[i] = (b_arr[i] - sum_new - sum_old) / A_arr[i, i]
```
Usa los valores más recientes calculados en la iteración actual (`x[:i]`) junto a los de la iteración previa (`x_old[i+1:]`) para obtener el valor actualizado de la incógnita $x_i$.

### 4.3 Cálculo de error relativo porcentual aproximado
```python
errors = np.zeros(n)
for i in range(n):
    if abs(x[i]) > 1e-12:
        errors[i] = abs((x[i] - x_old[i]) / x[i]) * 100
```
Calcula el error porcentual de cada variable comparando su valor actual con el anterior, y detiene el proceso si el error máximo es menor a la tolerancia dada (`max_err < tol`).

---

## 5. Ejemplo de verificación (Chapra 12.1)

Al correr el sistema de reactores acoplados con tolerancia de `1e-6` ($10^{-6}\%$):
* El código advierte que la matriz no cumple estrictamente con la DDE.
* El proceso converge en la **iteración 13** con un error máximo final de `3.4454e-07%`.
* El residuo final $\|Ax - b\|$ es virtualmente cero ($2.2970 \times 10^{-10}$), garantizando la exactitud de la aproximación.

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
from codigo.gauss_seidel import gauss_seidel

A = np.array([[4.0, 1.0], [2.0, 3.0]])
b = np.array([1.0, 2.0])

result = gauss_seidel(A, b, tol=1e-6, max_iter=150)
print("Convergió:", result["success"])
print("Solución aproximada:", result["solution"])
print("Cantidad de iteraciones:", len(result["iterations"]) - 1)
```
