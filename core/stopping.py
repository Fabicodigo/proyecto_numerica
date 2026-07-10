def criterio_parada(error=None, fx=None, iteracion=0, tol=1e-6, max_iter=150):
    if iteracion >= max_iter:
        return True, "Se alcanzó el máximo de iteraciones"

    if error is not None and abs(error) <= tol:
        return True, "Convergió por tolerancia del error"

    if fx is not None and abs(fx) <= tol:
        return True, "Convergió porque |f(x)| <= tolerancia"

    return False, ""