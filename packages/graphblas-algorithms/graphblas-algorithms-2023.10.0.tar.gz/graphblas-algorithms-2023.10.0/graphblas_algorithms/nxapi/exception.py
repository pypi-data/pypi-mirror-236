try:
    import networkx as nx
except ImportError:

    class NetworkXError(Exception):
        pass

    class NetworkXNoPath(Exception):
        pass

    class NetworkXPointlessConcept(Exception):
        pass

    class NetworkXUnbounded(Exception):
        pass

    class NodeNotFound(Exception):
        pass

    class PowerIterationFailedConvergence(Exception):
        pass

else:
    from networkx import (
        NetworkXError,
        NetworkXNoPath,
        NetworkXPointlessConcept,
        NetworkXUnbounded,
        NodeNotFound,
        PowerIterationFailedConvergence,
    )
try:
    import scipy as sp
except ImportError:

    class ArpackNoConvergence(Exception):
        def __init__(self, msg, eigenvalues, eigenvectors):
            super().__init__(msg)
            self.eigenvalues = eigenvalues
            self.eigenvectors = eigenvectors

else:
    from scipy.sparse.linalg import ArpackNoConvergence
