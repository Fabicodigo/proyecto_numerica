# Interpolación polinomial de Newton por diferencias divididas

Documento explicativo del script [`newton_interpolacion.py`](newton_interpolacion.py).
Implementa la **Figura 18.7** de Chapra & Canale, *Métodos numéricos para ingenieros*.

---

## 1. ¿Qué problema resuelve?

Dado un conjunto de `n+1` puntos de datos conocidos `(x₀, y₀), (x₁, y₁), …, (xₙ, yₙ)`,
queremos encontrar el **polinomio de grado ≤ n** que pasa exactamente por todos ellos y
usarlo para **estimar el valor de `y` en un punto `xi`** que no está en la tabla.

El método de Newton construye ese polinomio de forma **incremental**: primero el de grado 0
(una constante), luego el de grado 1 (recta), grado 2 (parábola), etc. Cada nuevo punto solo
**añade un término** al polinomio anterior, sin rehacer los cálculos previos.

La forma del polinomio de Newton es:

```
f(x) = b₀ + b₁(x - x₀) + b₂(x - x₀)(x - x₁) + … + bₙ(x - x₀)(x - x₁)…(x - xₙ₋₁)
```

donde cada coeficiente `bₖ` es una **diferencia dividida** de orden `k`.

---

## 2. Las diferencias divididas

Una diferencia dividida mide la "pendiente generalizada" entre puntos. Se definen
recursivamente:

- **Orden 0:** `f[xᵢ] = yᵢ` (el valor mismo).
- **Orden 1:** `f[xᵢ₊₁, xᵢ] = (f[xᵢ₊₁] − f[xᵢ]) / (xᵢ₊₁ − xᵢ)`
- **Orden j (general):**

```
f[xᵢ₊ⱼ, …, xᵢ] = ( f[xᵢ₊₁ … , orden j-1] − f[xᵢ … , orden j-1] ) / ( xᵢ₊ⱼ − xᵢ )
```

Es decir, cada diferencia dividida se obtiene de **dos diferencias adyacentes del orden
inmediatamente anterior**, dividiendo por la distancia entre los `x` de los extremos.

Los coeficientes del polinomio son los que quedan en la **primera fila** de la tabla:
`b₀ = fdd[0,0]`, `b₁ = fdd[0,1]`, `b₂ = fdd[0,2]`, …

### La tabla `fdd`

Se organiza como una matriz `(n+1) × (n+1)`. Solo se llena la **parte triangular superior**;
el resto queda en cero. Para el ejemplo del libro (4 puntos → matriz 4×4):

| i | col 0 (yᵢ) | col 1 | col 2 | col 3 |
|---|-----------|-------|-------|-------|
| 0 | y₀        | f[x₁,x₀] | f[x₂,x₁,x₀] | f[x₃,x₂,x₁,x₀] |
| 1 | y₁        | f[x₂,x₁] | f[x₃,x₂,x₁] | 0 |
| 2 | y₂        | f[x₃,x₂] | 0 | 0 |
| 3 | y₃        | 0 | 0 | 0 |

Fíjate en la forma de "escalera": cada columna `j` tiene una entrada menos que la anterior,
porque necesita `j+1` puntos para calcularse. La **diagonal superior (fila 0)** contiene los
coeficientes que usa el polinomio.

---

## 3. El punto delicado: la indexación (pseudocódigo → Python)

El pseudocódigo de Chapra está escrito con **bucles inclusivos** (`DOFOR i = 0, n` recorre
`0, 1, …, n`), mientras que `range` en Python es **exclusivo en el límite superior**
(`range(m)` recorre `0, 1, …, m-1`). Esta es la fuente más común de errores al traducir.

Convención clave:
- `n` en el pseudocódigo = **grado máximo** del polinomio.
- Hay `n+1` puntos de datos.
- En el código: `npts = len(x)` (= n+1) y `n = npts - 1`.

| Pseudocódigo (inclusivo) | Recorre | Python (exclusivo) |
|--------------------------|---------|--------------------|
| `DOFOR i = 0, n`         | 0 … n   | `for i in range(npts)` |
| `DOFOR j = 1, n`         | 1 … n   | `for j in range(1, npts)` |
| `DOFOR i = 0, n - j`     | 0 … n-j | `for i in range(npts - j)` |
| `DOFOR order = 1, n`     | 1 … n   | `for order in range(1, npts)` |

> **Regla mnemotécnica:** un `DOFOR a, b` inclusivo del libro se convierte en
> `range(a, b+1)` en Python. Como `b` casi siempre es `n` y `npts = n+1`, el `b+1`
> se vuelve `npts` de forma natural.

---

## 4. Recorrido del código, bloque por bloque

### 4.1 Preparación

```python
x = np.asarray(x, dtype=float)
y = np.asarray(y, dtype=float)
npts = len(x)      # n+1 puntos
n = npts - 1       # grado máximo
```

Se convierten las entradas a arreglos de `float` para evitar divisiones enteras y aceptar
tanto listas como arreglos de numpy.

### 4.2 Primera columna de la tabla

```python
fdd = np.zeros((npts, npts))
for i in range(npts):          # DOFOR i = 0, n
    fdd[i, 0] = y[i]
```

Las diferencias divididas de orden 0 son simplemente los valores `y`.

### 4.3 Rellenado de la tabla (parte triangular)

```python
for j in range(1, npts):       # DOFOR j = 1, n   (columnas)
    for i in range(npts - j):  # DOFOR i = 0, n-j (filas de esa columna)
        fdd[i, j] = (fdd[i+1, j-1] - fdd[i, j-1]) / (x[i+j] - x[i])
```

Traducción literal de la fórmula recursiva. El `npts - j` es lo que da la forma de escalera:
la columna `j` tiene `npts - j` entradas válidas.

### 4.4 Evaluación en `xi` acumulando por orden

```python
yint = np.zeros(npts)          # estimaciones de orden 0..n
ea   = np.full(npts, np.nan)   # error aproximado por orden
xterm = 1.0
yint[0] = fdd[0, 0]            # estimación de orden 0

for order in range(1, npts):   # DOFOR order = 1, n
    xterm = xterm * (xi - x[order-1])          # término acumulado
    yint2 = yint[order-1] + fdd[0, order] * xterm
    ea[order-1] = yint2 - yint[order-1]        # error aproximado
    yint[order] = yint2
```

- **`xterm`** es el producto acumulado `(xi − x₀)(xi − x₁)…`, que crece un factor por iteración.
- **`yint[order]`** es la estimación con el polinomio de grado `order`: la estimación previa
  más el nuevo término `bₖ · xterm`.
- **`ea[order-1]`** es el **error aproximado**: la diferencia entre dos estimaciones sucesivas.
  Como no conocemos el valor real, esta diferencia es la mejor medida de cuánto "cambió" la
  estimación al añadir un término más. La última posición (orden máximo) no tiene un término
  siguiente con el cual compararse, así que se deja como `NaN` y se imprime como `---`.

---

## 5. Valores de retorno

| Retorno | Tipo | Contenido |
|---------|------|-----------|
| `yint`  | `ndarray` de `n+1` | Estimación de grado 0, 1, …, n. `yint[-1]` es el resultado final de mayor orden. |
| `ea`    | `ndarray` de `n+1` | Error aproximado en cada orden. `ea[k] = yint[k+1] − yint[k]`. La última entrada es `NaN`. |

---

## 6. El ejemplo del libro (verificación)

Se estima `ln(2)` interpolando en `xi = 2` con los puntos:

```
x = [1, 4, 6, 5]
y = [0, 1.386294, 1.791759, 1.609438]
```

Salida del programa:

```
Orden |  Estimación yint |  Error aprox. (ea) |  Error verdadero
------------------------------------------------------------------
    0 |         0.000000 |           0.462098 |         100.000%
    1 |         0.462098 |           0.103746 |          33.333%
    2 |         0.565844 |           0.062923 |          18.366%
    3 |         0.628767 |                --- |           9.288%

Resultado final (mayor orden): 0.628767
```

Estos valores (0.462098 → 0.565844 → 0.628767) coinciden exactamente con los reportados por
Chapra. El valor real es `ln(2) = 0.693147`; el polinomio de grado 3 lo aproxima con un error
verdadero del 9.3 %.

**Observación didáctica:** el orden de los puntos importa para las estimaciones intermedias y
el error aproximado, pero **el polinomio final de grado n es el mismo** independientemente del
orden (todos los puntos quedan incluidos). Los puntos `[1, 4, 6, 5]` no están ordenados: es
justamente el caso del libro para ilustrar cómo el error va decreciendo al ir añadiendo puntos.

---

## 7. La gráfica

El bloque final (dentro de un `try/except ImportError`) dibuja:

- **Curva azul:** el polinomio interpolante de grado 3, evaluado en 300 puntos de una malla fina.
- **Puntos rojos:** los datos conocidos.
- **Punto verde:** la interpolación en `xi = 2`.
- **Línea gris punteada:** la función real `ln(x)`, como referencia para ver el error.

`matplotlib` ya está instalado en tu entorno, así que al ejecutar el script se abrirá la
ventana de la gráfica con `plt.show()`.

---

## 8. Cómo ejecutarlo

```powershell
python newton_interpolacion.py
```

> **Nota sobre acentos en la terminal de Windows:** si ves caracteres raros como
> `Interpolaci�n`, ejecuta antes `chcp 65001` para cambiar la consola a UTF-8. El archivo
> fuente está correctamente codificado; es solo un tema de visualización de la consola.

### Usar la función desde otro script

```python
import numpy as np
from newton_interpolacion import newt_int

x = np.array([1, 4, 6, 5])
y = np.array([0, 1.386294, 1.791759, 1.609438])

yint, ea = newt_int(x, y, xi=2)
print("Estimación final:", yint[-1])   # 0.628767
```
