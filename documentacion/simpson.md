# Reglas de Simpson (integración numérica)

Documento explicativo del script [`simpson.py`](simpson.py).
Implementa la **Figura 21.13** de Chapra & Canale, *Métodos numéricos para ingenieros*.

---

## 1. ¿Qué problema resuelve?

Igual que el trapecio: aproximar `∫ₐᵇ f(x) dx`. La diferencia es que **en vez de rectas,
Simpson ajusta parábolas o cúbicas** a los nodos. Como los polinomios de mayor grado siguen
mejor las curvas, el error es mucho menor para el mismo número de puntos.

- **Simpson 1/3** → ajusta una **parábola** (grado 2) usando grupos de **3 nodos** (2 segmentos).
- **Simpson 3/8** → ajusta una **cúbica** (grado 3) usando grupos de **4 nodos** (3 segmentos).

Ambas son fórmulas de **Newton-Cotes** de orden superior al trapecio.

---

## 2. Las fórmulas

### a) Simpson 1/3 simple (3 puntos, 2 segmentos)

```
I ≈ 2h · (f₀ + 4f₁ + f₂) / 6
```

El punto central `f₁` pesa 4; los extremos pesan 1. El `2h` es el ancho total de los dos
segmentos.

### b) Simpson 3/8 simple (4 puntos, 3 segmentos)

```
I ≈ 3h · (f₀ + 3(f₁ + f₂) + f₃) / 8
```

Los dos puntos interiores pesan 3; los extremos pesan 1.

### c) Simpson 1/3 múltiple (n par)

```
        h
I ≈  ───── · [ f₀ + 4(f₁+f₃+…+fₙ₋₁) + 2(f₂+f₄+…+fₙ₋₂) + fₙ ]
        3
```

- Nodos de **índice impar** (los vértices de cada parábola) pesan **4**.
- Nodos de **índice par interior** (uniones entre parábolas) pesan **2**.
- Extremos pesan **1**.
- **`n` debe ser par**, porque cada parábola consume 2 segmentos.

---

## 3. La lógica de la función maestra `simp_int`

Este es el corazón del algoritmo y lo más importante para estudiar. El problema: Simpson 1/3
solo sirve si `n` es **par**. ¿Qué hacemos si `n` es impar? La respuesta de Chapra:

```
Si n = 1        -> usar el TRAPECIO (no hay puntos para una parábola).
Si n es PAR     -> Simpson 1/3 múltiple, directo.
Si n es IMPAR   -> aplicar Simpson 3/8 a los ÚLTIMOS 3 segmentos (que consumen
                   el "sobrante" impar) y Simpson 1/3 múltiple a los primeros
                   m = n - 3 segmentos (que ya son un número par).
```

El truco: **3/8 usa 3 segmentos (impar)**. Al quitarle 3 segmentos a un `n` impar, queda
`m = n - 3` **par**, apto para 1/3. Así se cubre cualquier `n` combinando ambas reglas.

### El nodo compartido

Los primeros `m` segmentos usan los nodos `f[0] … f[m]`. Los últimos 3 usan `f[n-3] … f[n]`.
Como `m = n - 3`, el nodo **`f[m] = f[n-3]` es compartido**: es el final de la parte 1/3 y el
inicio de la parte 3/8. Esto es correcto: una integral cubre `[x₀, xₘ]` y la otra `[xₘ, xₙ]`,
y sumarlas da el total.

---

## 4. La indexación (el punto más delicado)

El pseudocódigo indexa `f[0] … f[n]`. En Python el arreglo tiene `n+1` elementos con esos
mismos índices, así que `f[n]` es el último. Puntos a cuidar:

### 4.1 El bucle de Simpson 1/3 múltiple

```
DOFOR i = 1, n-2, 2       <- inclusivo, con PASO 2: recorre 1, 3, …, n-3
```

| Pseudocódigo (inclusivo, paso 2) | Recorre | Python |
|----------------------------------|---------|--------|
| `DOFOR i = 1, n-2, 2`            | 1,3,…,n-3 | `for i in range(1, n-1, 2)` |

`range(1, n-1, 2)` **excluye** `n-1`, por lo que el último `i` es `n-3` (para `n` par).
Dentro se suma `4*f[i] + 2*f[i+1]`, y **fuera del bucle** se agrega `4*f[n-1] + f[n]` (el
último vértice y el extremo derecho).

### 4.2 Los últimos 4 nodos para Simpson 3/8

```python
simp38(h, f[n-3], f[n-2], f[n-1], f[n])
```

Estos son exactamente los **4 últimos elementos** del arreglo. Verificado: para `n=5`,
`f[2], f[3], f[4], f[5]`.

### 4.3 Simpson 1/3 sobre los primeros m segmentos

```python
simp13m(h, m, f)      # se pasa el arreglo COMPLETO, pero con n = m
```

Funciona porque `simp13m` **solo accede a los índices `0 … m`** del arreglo (nunca más allá),
que son justamente los primeros `m+1` nodos. No hay que recortar el arreglo.

---

## 5. Recorrido del código, bloque por bloque

- **`trap(h, f0, f1)`** — trapecio simple; solo se usa si `n = 1`.
- **`simp13` / `simp38`** — traducción literal de las fórmulas simples.
- **`simp13m(h, n, f)`** — inicia `suma = f[0]`, recorre impares con `range(1, n-1, 2)` sumando
  `4*f[i]+2*f[i+1]`, cierra con `4*f[n-1]+f[n]`, y devuelve `h*suma/3`.
- **`simp_int(a, b, n, f)`** — inicia `suma = 0`, calcula `h`, y aplica la lógica de la
  sección 3. Detecta impar con `n % 2 == 1` (equivalente al `odd = n/2 - INT(n/2)` del libro).
- **`simp_int_func(func, a, b, n)`** — genera los `n+1` nodos con `np.linspace(a, b, n+1)`,
  evalúa `func`, y delega en `simp_int`.

---

## 6. El ejemplo del libro (verificación)

Polinomio de grado 5 en `[0, 0.8]`, valor **exacto = 1.640533**.

```
Método                               Estimación   Error rel. %
--------------------------------------------------------------
Simpson 1/3 simple (n=2)               1.367467       16.6450%
Simpson 3/8 simple (n=3)               1.519170        7.3978%
simp_int (n=4, 1/3 múltiple)           1.623467        1.0403%
simp_int (n=5, 3/8 + 1/3 múltiple)     1.645077        0.2770%
simp_int (n=6, 1/3 múltiple)           1.637162        0.2055%
```

Observaciones para estudiar:

- **Simpson es muchísimo más preciso que el trapecio.** Con el trapecio, `n=4` daba 9.5% de
  error; con Simpson 1/3, `n=4` da apenas **1.04%**.
- El caso clave **`n=5`** confirma que la función maestra combina bien 3/8 + 1/3 (error 0.28%).
- **¿Por qué n=2 (16.6%) tiene más error que n=3 (7.4%)?** Con n=2 hay una sola parábola para
  cubrir todo `[0, 0.8]`, muy poca resolución para un polinomio de grado 5. No es que 3/8 sea
  "mejor" que 1/3 en general; es que con más segmentos y nodos hay más resolución.
- El error de Simpson 1/3 múltiple es **O(h⁴)**: al duplicar `n` el error tiende a caer a 1/16,
  mucho más rápido que el O(h²) del trapecio.

---

## 7. Comparación de las tres cuadraturas vistas

| Regla | Ajusta | Nodos por tramo | Orden del error | Restricción sobre n |
|-------|--------|-----------------|-----------------|---------------------|
| Trapecio | recta (grado 1) | 2 | O(h²) | cualquiera |
| Simpson 1/3 | parábola (grado 2) | 3 | O(h⁴) | n **par** |
| Simpson 3/8 | cúbica (grado 3) | 4 | O(h⁴) | n múltiplo de 3 |

`simp_int` combina 1/3 y 3/8 para aceptar **cualquier `n`**, aprovechando la alta precisión de
Simpson sin la restricción de paridad.

---

## 8. La gráfica

El bloque final dibuja la función real `f(x)` con su área sombreada y marca los `n+1` nodos
(con `n = 6`) que Simpson usa para el ajuste. `matplotlib` ya está instalado.

---

## 9. Cómo ejecutarlo

```powershell
python simpson.py
```

> **Acentos en consola Windows:** si ves `M�todo`, ejecuta antes `chcp 65001` (consola UTF-8).
> El archivo fuente está bien codificado.

### Usar las funciones desde otro script

```python
import numpy as np
from simpson import simp_int_func, simp13, simp38

# Integrar una función con la maestra (elige la regla sola):
I = simp_int_func(np.sin, 0, np.pi, n=10)   # ≈ 2.0

# Reglas simples directas:
I13 = simp13(h=0.4, f0=0.2, f1=2.456, f2=0.232)
```
