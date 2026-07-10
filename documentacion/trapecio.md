# Regla del trapecio (integración numérica)

Documento explicativo del script [`trapecio.py`](trapecio.py).
Implementa la **Figura 21.9** de Chapra & Canale, *Métodos numéricos para ingenieros*.

---

## 1. ¿Qué problema resuelve?

Queremos calcular una **integral definida** `∫ₐᵇ f(x) dx` (el área bajo la curva) cuando no es
práctico o posible hacerlo analíticamente. La idea de la regla del trapecio es **reemplazar la
curva por segmentos de recta** y sumar las áreas de los trapecios que se forman.

Es la más simple de las **fórmulas de Newton-Cotes**: aproxima `f(x)` por un polinomio de
grado 1 (una recta) en cada segmento.

---

## 2. La fórmula

### a) Un solo segmento

El área de un trapecio es *ancho × promedio de las alturas*:

```
I ≈ h · (f(a) + f(b)) / 2        con  h = b − a
```

Los dos "lados" del trapecio son `f(a)` y `f(b)`, y la base es el ancho `h`. Es una recta
uniendo los dos extremos: si la curva se aleja mucho de esa recta, el error es grande.

### b) Segmentos múltiples

Si dividimos `[a, b]` en `n` segmentos iguales de ancho `h = (b−a)/n`, tenemos **n+1 nodos**
`x₀, x₁, …, xₙ` y aplicamos un trapecio en cada tramo. Al sumarlos:

```
        h
I ≈  ───── · [ f(x₀)  +  2·(f(x₁) + f(x₂) + … + f(xₙ₋₁))  +  f(xₙ) ]
        2
```

**¿Por qué los interiores van multiplicados por 2?** Cada nodo interior es compartido por dos
trapecios adyacentes (es el extremo derecho de uno y el izquierdo del siguiente), así que su
altura se cuenta **dos veces**. Los extremos `x₀` y `xₙ` pertenecen a un solo trapecio, por eso
se cuentan **una sola vez**.

---

## 3. Indexación: pseudocódigo → Python

El punto delicado es el bucle de los nodos interiores. El pseudocódigo:

```
sum = f0
DOFOR i = 1, n - 1        <- inclusivo: recorre 1, 2, …, n-1
  sum = sum + 2 * f[i]
END DO
sum = sum + f[n]
```

| Pseudocódigo (inclusivo) | Recorre | Python (exclusivo) |
|--------------------------|---------|--------------------|
| `DOFOR i = 1, n-1`       | 1 … n-1 | `for i in range(1, n)` |

Recordá que `range(1, n)` **no incluye** `n`, así que recorre exactamente `1, 2, …, n-1`, que
son los nodos **interiores**. Los extremos `f[0]` y `f[n]` se suman aparte, fuera del bucle.

> **Cuidado clásico de examen:** `n` aquí NO es el número de nodos, es el **número de
> segmentos**. Los nodos son `n+1` (de `f[0]` a `f[n]`). Confundir esto es el error más común.

---

## 4. Recorrido del código, bloque por bloque

### 4.1 `trap(h, f0, f1)` — un solo segmento

```python
def trap(h, f0, f1):
    return h * (f0 + f1) / 2
```

Traducción literal de la fórmula del trapecio único. Recibe directamente el ancho y las dos
alturas.

### 4.2 `trapm(h, n, f)` — múltiples segmentos

```python
f = np.asarray(f, dtype=float)
suma = f[0]                     # extremo izquierdo (x1)
for i in range(1, n):           # DOFOR i = 1, n-1
    suma = suma + 2 * f[i]      # interiores, contados doble
suma = suma + f[n]              # extremo derecho, una vez
return h * suma / 2             # factor común h/2
```

Cada línea corresponde 1:1 con el pseudocódigo. El `range(1, n)` reproduce `DOFOR i = 1, n-1`.

### 4.3 `trapm_func(func, a, b, n)` — conveniencia

```python
h = (b - a) / n                 # ancho de cada segmento
x = np.linspace(a, b, n + 1)    # n+1 nodos equiespaciados
f = func(x)                     # valores de la función en los nodos
return trapm(h, n, f)           # delega en trapm
```

Sirve para integrar una función directamente sin tener que generar a mano los nodos y sus
valores. `np.linspace(a, b, n+1)` genera exactamente **n+1** puntos (¡no `n`!), porque hay un
nodo más que segmentos.

---

## 5. El ejemplo del libro (verificación)

Se integra el polinomio de grado 5:

```
f(x) = 0.2 + 25x − 200x² + 675x³ − 900x⁴ + 400x⁵
```

en `[0, 0.8]`, cuyo valor **exacto** es `1.640533`.

Salida del programa:

```
Método                          Estimación    Error rel. %
----------------------------------------------------------
1 segmento  (trap)                0.172800         89.467%
2 segmentos (trapm)               1.068800         34.850%
4 segmentos (trapm)               1.484800          9.493%
```

Coincide con Chapra. Observaciones para estudiar:

- Con **1 segmento** el error es enorme (89%): una sola recta no puede seguir un polinomio de
  grado 5 que sube y baja dentro del intervalo.
- Al **duplicar** los segmentos, el error baja de forma marcada (89% → 35% → 9%).
- El error de la regla del trapecio compuesta es **O(h²)**: al reducir `h` a la mitad
  (duplicar `n`), el error tiende a reducirse aproximadamente a **la cuarta parte**. Se aprecia
  entre n=2 y n=4 (34.9% → 9.5%, ≈ ÷3.7, cercano a ÷4; no es exacto porque el integrando no es
  una parábola pura).

---

## 6. La gráfica

El bloque final (protegido con `try/except ImportError`) dibuja:

- **Curva azul:** la función real `f(x)`.
- **Línea roja con marcadores:** los segmentos de recta que unen los nodos (con `n = 4`); cada
  tramo entre dos nodos es la tapa superior de un trapecio.
- **Relleno rojo:** el área que efectivamente estima la regla del trapecio.

Comparar visualmente el relleno con el área bajo la curva azul deja ver de dónde viene el
error.

---

## 7. Cómo ejecutarlo

```powershell
python trapecio.py
```

> **Acentos en consola Windows:** si ves `M�todo`, ejecuta antes `chcp 65001` para poner la
> consola en UTF-8. El archivo fuente está bien codificado en UTF-8.

### Usar las funciones desde otro script

```python
import numpy as np
from trapecio import trap, trapm, trapm_func

# Integrar una función directamente:
I = trapm_func(np.sin, 0, np.pi, n=100)
print(I)   # ≈ 2.0

# O con valores tabulados en los nodos:
f = [0, 1, 4, 9, 16]      # 5 valores -> n = 4 segmentos
I2 = trapm(h=1, n=4, f=f)
```
