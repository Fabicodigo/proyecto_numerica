# Interpolación polinomial de Lagrange

Documento explicativo del script [`lagrange_interpolacion.py`](lagrange_interpolacion.py).
Implementa la **Figura 18.11** de Chapra & Canale, *Métodos numéricos para ingenieros*.

---

## 1. ¿Qué problema resuelve?

Igual que el método de Newton: dados `n+1` puntos de datos conocidos
`(x₀, y₀), …, (xₙ, yₙ)`, buscamos el polinomio de grado ≤ n que pasa por todos ellos y lo
usamos para **estimar `y` en un punto `xi`** que no está en la tabla.

La diferencia es la **forma de escribir el polinomio**. Lagrange no calcula coeficientes ni
construye tablas: expresa el polinomio directamente como una **combinación ponderada de los
valores `yᵢ`**.

> **Dato clave:** el polinomio interpolante de grado n por un conjunto de puntos es **único**.
> Newton y Lagrange dan *exactamente el mismo polinomio*; solo cambian la manera de calcularlo.
> Por eso interpolar `ln(2)` con los puntos `[1, 4, 6]` da `0.565844` con ambos métodos.

---

## 2. La idea: polinomios base

El polinomio de Lagrange se escribe así:

```
f(xi) = Σ  yᵢ · Lᵢ(xi)          (suma para i = 0 … n)
        i
```

Cada `Lᵢ(xi)` es un **polinomio base de Lagrange**, definido como:

```
        n     (xi − xⱼ)
Lᵢ(xi) = Π   ───────────       (producto para j = 0 … n, con j ≠ i)
       j≠i   (xᵢ − xⱼ)
```

### La propiedad mágica de los polinomios base

Cada `Lᵢ` está diseñado para cumplir:

- **`Lᵢ(xᵢ) = 1`** — en su propio nodo vale exactamente 1.
- **`Lᵢ(xₖ) = 0`** para todo `k ≠ i` — en los demás nodos vale exactamente 0.

¿Por qué? Mira el factor `(xi − xⱼ)/(xᵢ − xⱼ)`:

- Si evalúas en `xi = xᵢ` (su propio nodo), cada factor es `(xᵢ − xⱼ)/(xᵢ − xⱼ) = 1`, así que
  el producto entero es 1.
- Si evalúas en `xi = xₖ` (otro nodo, con `k ≠ i`), uno de los factores del producto es
  `(xₖ − xₖ)/(xᵢ − xₖ) = 0`, y todo el producto se anula.

Gracias a esto, al sumar `Σ yᵢ·Lᵢ(xi)`, en cada nodo `xₖ` sobrevive solo el término `yₖ·1` y
el resto se cancela → el polinomio **pasa exactamente por todos los puntos**.

### ¿Por qué la condición `j ≠ i` es obligatoria?

Si no se excluyera `j = i`, aparecería el factor `(xi − xᵢ)/(xᵢ − xᵢ)`, cuyo denominador es
`xᵢ − xᵢ = 0` → **división por cero**. La condición `i != j` del pseudocódigo es exactamente
lo que evita eso y lo que da la forma correcta al polinomio base.

---

## 3. Sobre los nombres (la ambigüedad del pseudocódigo)

El pseudocódigo del libro reza `FUNCTION Lagrng(x, y, n, x)`: usa **`x` dos veces**, para el
arreglo de datos y para el punto de evaluación. Es ambiguo y en Python causaría que un nombre
tape al otro.

En el código se desambigua:

| Pseudocódigo | Python | Significado |
|--------------|--------|-------------|
| `x` (arreglo) | `x`  | abscisas de los puntos de datos |
| `x` (escalar) | `xi` | punto donde se interpola |

---

## 4. Indexación: pseudocódigo → Python

Como en Newton, los bucles del libro son **inclusivos** (`DOFOR i = 0, n` recorre `0…n`) y
`range` en Python es **exclusivo** en el límite superior.

| Pseudocódigo (inclusivo) | Recorre | Python (exclusivo) |
|--------------------------|---------|--------------------|
| `DOFOR i = 0, n`         | 0 … n   | `for i in range(npts)` |
| `DOFOR j = 0, n`         | 0 … n   | `for j in range(npts)` |

Con `npts = len(x)` (= n+1) y `n = npts - 1` como el grado. La regla sigue siendo:
`DOFOR a, b` inclusivo → `range(a, b+1)`, y como `b = n`, queda `range(npts)`.

---

## 5. Recorrido del código, bloque por bloque

### 5.1 Preparación

```python
x = np.asarray(x, dtype=float)
y = np.asarray(y, dtype=float)
npts = len(x)   # n+1 puntos
suma = 0.0      # acumulador de la sumatoria
```

Se convierte a `float` para evitar divisiones enteras. `suma` es el `sum` del pseudocódigo.

### 5.2 Bucle externo — recorre los puntos

```python
for i in range(npts):          # DOFOR i = 0, n
    product = y[i]             # arranca en yᵢ
```

Cada iteración construye un término `yᵢ · Lᵢ(xi)`. Se parte de `product = y[i]` y luego se
multiplica por el polinomio base.

### 5.3 Bucle interno — construye el polinomio base

```python
    for j in range(npts):      # DOFOR j = 0, n
        if i != j:             # se omite el factor j = i
            product = product * (xi - x[j]) / (x[i] - x[j])
```

Multiplica acumulativamente los factores `(xi − xⱼ)/(xᵢ − xⱼ)` para todo `j ≠ i`, obteniendo
`yᵢ · Lᵢ(xi)`.

### 5.4 Acumulación

```python
    suma = suma + product
return suma
```

Se suma el término del punto `i` y, al terminar, `suma` contiene `f(xi)`.

---

## 6. El ejemplo del libro (verificación)

Se estima `ln(2)` interpolando en `xi = 2` con **tres puntos** (grado 2):

```
x = [1, 4, 6]
y = [0, 1.386294, 1.791759]
```

Salida del programa:

```
Estimación f(2)   = 0.565844
Valor real ln(2)  = 0.693147
Error verdadero   = 18.366%
```

El valor `0.565844` coincide con Chapra y con la estimación de orden 2 del método de Newton
(mismo polinomio, distinta forma de calcularlo).

---

## 7. Newton vs. Lagrange (comparación de estudio)

| Aspecto | Newton (dif. divididas) | Lagrange |
|---------|-------------------------|----------|
| Polinomio resultante | El mismo | El mismo |
| Cómo se calcula | Tabla de diferencias divididas + coeficientes | Suma directa de términos ponderados |
| Estimaciones intermedias | Sí (orden 0, 1, …, n) y error aproximado | No de forma natural (evalúa el grado n completo) |
| Añadir un punto nuevo | Fácil: solo se agrega un término | Hay que recalcular todos los `Lᵢ` |
| Ventaja principal | Eficiente e incremental; da el error aproximado | Fórmula compacta y directa; ideal para deducciones teóricas |

**Regla práctica del libro:** Newton suele preferirse cuando importa estimar el error o ir
añadiendo puntos; Lagrange es más limpio conceptualmente y cuando el grado ya está fijado.

---

## 8. La gráfica

El bloque final (protegido con `try/except ImportError`) dibuja:

- **Curva azul:** el polinomio de Lagrange (grado 2), evaluado en 300 puntos de una malla fina.
- **Puntos rojos:** los datos conocidos.
- **Punto verde:** la interpolación en `xi = 2`.
- **Línea gris punteada:** la función real `ln(x)`, como referencia del error.

`matplotlib` ya está instalado, así que `python lagrange_interpolacion.py` abrirá la ventana.

---

## 9. Cómo ejecutarlo

```powershell
python lagrange_interpolacion.py
```

> **Acentos en consola Windows:** si ves `Interpolaci�n`, ejecuta antes `chcp 65001` para
> cambiar la consola a UTF-8. El archivo fuente está correctamente codificado en UTF-8.

### Usar la función desde otro script

```python
import numpy as np
from lagrange_interpolacion import lagrange

x = np.array([1, 4, 6])
y = np.array([0, 1.386294, 1.791759])

estimacion = lagrange(x, y, xi=2)
print(estimacion)   # 0.565844
```
