# Guía de problemas 18 resuelta con código (18.5, 18.8 y 18.8)

Documento explicativo del módulo [`guia_problemas_18.py`](../codigo/guia_problemas_18.py).
Resuelve **con el código del proyecto** los problemas 18.5, 18.8 y 18.8 de
Chapra & Canale, *Métodos numéricos para ingenieros* (Capítulo 18, Interpolación).

La idea central: **no se reescribe ningún método**. El módulo reutiliza las
implementaciones ya existentes en el proyecto y solo las *orquesta* para cada
problema:

| Problema | Método | Función reutilizada | Archivo |
|----------|--------|--------------------|---------|
| 18.5 | Newton (diferencias divididas) | `newt_int` | `codigo/newton_interpolacion.py` |
| 18.8 | Lagrange | `lagrange` | `codigo/lagrange_interpolacion.py` |
| 18.8 | Interpolación inversa | `newt_int` + `biseccion` | `codigo/biseccion.py` |

## Cómo ejecutarlo desde el menú

```
python main.py
  -> 3. Interpolación
     -> 3. Resolver Guía de Problemas 18 (18.5, 18.8, 18.8)
```

El submenú permite ejecutar cada problema por separado o todos de una vez,
y para el 18.8 pregunta si se desea la graficación interactiva paso a paso
de la bisección (igual que los ejercicios predefinidos de raíces).

---

## 1. Datos comunes (18.5 y 18.8)

```
x    = [1, 2, 3, 5, 7, 8]
f(x) = [3, 6, 19, 99, 291, 444]
```

Se quiere estimar `f(4)`. Los datos provienen exactamente del polinomio cúbico
`f(x) = x³ − x² − x + 4`, así que el **valor verdadero es `f(4) = 48`** y sirve
como referencia para verificar el código.

---

## 2. Problema 18.5 — Newton con `newt_int`

### La clave: el orden de los puntos

`newt_int` construye el polinomio de forma incremental: el orden `k` usa los
primeros `k+1` puntos del arreglo. Por eso, para que cada orden use los puntos
**más cercanos a `xi = 4`**, se pasan ordenados por proximidad:

```python
x = [3, 5, 2, 7, 1]
y = [19, 99, 6, 291, 3]
yint, ea = newt_int(x, y, 4.0)
```

Una sola llamada devuelve **todas las estimaciones de orden 0 a 4** (`yint`) y
el error aproximado de cada una (`ea`):

```
Orden |  Estimación f(4) |  Error aprox. (ea)
----------------------------------------------
    1 |        59.000000 |          -9.000000
    2 |        50.000000 |          -2.000000
    3 |        48.000000 |           0.000000
    4 |        48.000000 |                ---
```

Coincide con el cálculo manual de la guía: `f₁(4) = 59`, `f₂(4) = 50`,
`f₃(4) = 48`, `f₄(4) = 48`. El error aproximado se anula a partir del orden 3
porque `b₄ = 0`: la señal práctica de que **un cúbico basta**.

---

## 3. Problema 18.8 — Lagrange con `lagrange`

A diferencia de Newton, `lagrange` devuelve **una sola estimación** para un
conjunto fijo de nodos. Cambiar de orden implica recalcular todo, así que se
hace **una llamada por orden**, con los nodos más cercanos a `xi = 4`:

```python
lagrange([3, 5],        [19, 99],         4.0)   # orden 1 -> 59
lagrange([2, 3, 5],     [6, 19, 99],      4.0)   # orden 2 -> 50
lagrange([2, 3, 5, 7],  [6, 19, 99, 291], 4.0)   # orden 3 -> 48
```

El módulo imprime además la comparación con Newton:

```
Orden |     Newton |   Lagrange
---------------------------------
    1 |  59.000000 |  59.000000
    2 |  50.000000 |  50.000000
    3 |  48.000000 |  48.000000
```

**Son idénticos y no es casualidad**: el polinomio interpolante de grado `n`
por un conjunto de puntos es único; Newton y Lagrange son dos escrituras del
mismo polinomio. La diferencia es práctica:

- **Newton** reutiliza cálculos y entrega el error de cada orden → ideal para
  explorar qué grado se necesita (una llamada, todas las respuestas).
- **Lagrange** es compacto, pero cada orden es un cálculo desde cero → ideal
  cuando el grado ya está fijado (tres llamadas separadas).

Esta asimetría se ve directamente en el código: 18.5 es *una* llamada a
`newt_int`; 18.8 son *tres* llamadas a `lagrange`.

---

## 4. Problema 18.8 — Interpolación inversa (cúbica + bisección)

### El problema

Datos de `f(x) = 1/x` (se corrige el error de transcripción del enunciado:
`f(7) = 0.1429`, no `1.1429`):

```
x    = [2, 3, 4, 5, 6, 7]
f(x) = [0.5, 0.3333, 0.25, 0.2, 0.1667, 0.1429]
```

Se busca el `x` tal que `f(x) = 0.23`. Como `f(4) = 0.25 > 0.23 > 0.2 = f(5)`,
la respuesta está en `[4, 5]`.

### La combinación de dos métodos del proyecto

1. **Interpolación:** se construye el cúbico `p(x)` con los 4 puntos más
   cercanos `{3, 4, 5, 6}`. En el código, `p(x)` es simplemente `newt_int`
   evaluado tomando la estimación de mayor orden:

   ```python
   def p(x):
       return newt_int([3, 4, 5, 6], [0.3333, 0.25, 0.2, 0.1667], x)[0][-1]
   ```

2. **Raíces:** no se puede "despejar" `x` de `p(x) = 0.23`, así que se define
   `g(x) = p(x) − 0.23` y se le pasa directamente a la **`biseccion` del
   proyecto** en `[4, 5]` (hay cambio de signo: `g(4) = +0.02`,
   `g(5) = −0.03`):

   ```python
   resultado = biseccion(g, 4.0, 5.0, tol=1e-5, plot_evolution=plot_evolution)
   ```

La bisección imprime su tabla de iteraciones habitual y converge en 9
iteraciones (criterio `|f(x)| <= tol` con `tol = 1e-5`):

```
Valor al que converge: 4.3417968750
```

**Resultado: `x ≈ 4.3418`.** El valor real es `1/0.23 = 4.3478`; la pequeña
diferencia (~0.14 %) viene del redondeo de la tabla (4 decimales) y de que el
cúbico es una aproximación de `1/x`, no la función exacta.

> **Idea clave:** la interpolación inversa transforma un problema donde
> "no puedes despejar `x`" en uno de **búsqueda de raíces**, que sí se
> resuelve con bisección. Es el ejemplo de cómo se **combinan dos métodos
> numéricos** — y en el código se ve literal: `g(x)` envuelve a `newt_int` y
> `biseccion` itera sobre `g`.

### Nota sobre la guía manual

La guía de estudio en papel corta la bisección en 6 iteraciones (error
aproximado 0.36 %) y reporta `x ≈ 4.33`. El código, con la tolerancia estándar
del proyecto (`1e-5`), afina hasta `x ≈ 4.3418`: es el mismo proceso, solo con
un criterio de parada más exigente. Ambos caen en el rango esperado 4.33–4.35.

---

## 5. Resumen de resultados

| Problema | Pregunta | Respuesta del código | Verificación |
|----------|----------|----------------------|--------------|
| 18.5 | `f(4)` con Newton, órdenes 1–4 | 59, 50, **48**, 48 | `f(4) = 48` exacto (datos cúbicos) |
| 18.8 | `f(4)` con Lagrange, órdenes 1–3 | 59, 50, **48** | idéntico a Newton (unicidad) |
| 18.8 | `x` tal que `f(x) = 0.23` | **x ≈ 4.3418** | valor real `1/0.23 = 4.3478` |
