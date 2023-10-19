from graphblas_algorithms import algorithms
from graphblas_algorithms.classes.digraph import to_graph

from ..exception import PowerIterationFailedConvergence

_all = ["pagerank", "google_matrix"]


def pagerank(
    G,
    alpha=0.85,
    personalization=None,
    max_iter=100,
    tol=1e-06,
    nstart=None,
    weight="weight",
    dangling=None,
):
    G = to_graph(G, weight=weight, dtype=float)
    N = len(G)
    if N == 0:
        return {}
    # We'll normalize initial, personalization, and dangling vectors later
    x = G.dict_to_vector(nstart, dtype=float, name="nstart")
    p = G.dict_to_vector(personalization, dtype=float, name="personalization")
    row_degrees = G.get_property("plus_rowwise+")  # XXX: What about self-edges?
    if dangling is not None and row_degrees.nvals < N:
        dangling_weights = G.dict_to_vector(dangling, dtype=float, name="dangling")
    else:
        dangling_weights = None
    try:
        result = algorithms.pagerank(
            G,
            alpha=alpha,
            personalization=p,
            max_iter=max_iter,
            tol=tol,
            nstart=x,
            dangling=dangling_weights,
            row_degrees=row_degrees,
        )
    except algorithms.exceptions.ConvergenceFailure as e:
        raise PowerIterationFailedConvergence(*e.args) from e
    else:
        return G.vector_to_nodemap(result, fill_value=0.0)


def google_matrix(
    G, alpha=0.85, personalization=None, nodelist=None, weight="weight", dangling=None
):
    G = to_graph(G, weight=weight, dtype=float)
    p = G.dict_to_vector(personalization, dtype=float, name="personalization")
    if dangling is not None and G.get_property("row_degrees+").nvals < len(G):
        dangling_weights = G.dict_to_vector(dangling, dtype=float, name="dangling")
    else:
        dangling_weights = None
    return algorithms.google_matrix(
        G,
        alpha=alpha,
        personalization=p,
        nodelist=nodelist,
        dangling=dangling_weights,
    )
