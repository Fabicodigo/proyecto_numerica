import numpy as np

def construir_funcion(expr):
    def f(x):
        resultado = eval(expr, {
            "__builtins__": {},
            "x": x,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "pi": np.pi,
            "e": np.e
        })

        # Si el resultado es escalar, lo adapta al tamaño de x
        if np.isscalar(resultado):
            if np.isscalar(x):
                return float(resultado)
            return np.full_like(np.asarray(x, dtype=float), float(resultado), dtype=float)

        return resultado

    return f