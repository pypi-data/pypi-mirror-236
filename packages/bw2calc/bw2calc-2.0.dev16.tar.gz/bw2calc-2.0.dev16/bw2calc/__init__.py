__all__ = [
    "ComparativeMonteCarlo",
    "DenseLCA",
    "direct_solving_worker",
    # "DirectSolvingMixin",
    # "DirectSolvingMonteCarloLCA",
    "GraphTraversal",
    "LCA",
    "LeastSquaresLCA",
    # "load_calculation_package",
    # "MonteCarloLCA",
    "MultiLCA",
    "MultifunctionalGraphTraversal",
    # "MultiMonteCarlo",
    # "ParallelMonteCarlo",
    # "ParameterVectorLCA",
    # "save_calculation_package",
]

__version__ = "2.0.DEV16"

try:
    import json_logging

    json_logging.init_non_web(enable_json=True)
except ImportError:
    pass


try:
    from pypardiso import factorized, spsolve

    PYPARDISO = True
except ImportError:
    from scipy.sparse.linalg import factorized, spsolve

    PYPARDISO = False
try:
    from presamples import PackagesDataLoader
except ImportError:
    PackagesDataLoader = None
try:
    from bw2data import __version__ as _bw2data_version
    from bw2data import prepare_lca_inputs, get_activity

    if not _bw2data_version >= (4, 0):
        raise ImportError
except ImportError:
    prepare_lca_inputs = get_activity = None


from .dense_lca import DenseLCA
from .lca import LCA
from .graph_traversal import GraphTraversal, MultifunctionalGraphTraversal
from .least_squares import LeastSquaresLCA
from .multi_lca import MultiLCA

# from .utils import save_calculation_package, load_calculation_package

try:
    from .mc_vector import ParameterVectorLCA
    from .monte_carlo import (
        ComparativeMonteCarlo,
        DirectSolvingMixin,
        DirectSolvingMonteCarloLCA,
        MonteCarloLCA,
        MultiMonteCarlo,
        ParallelMonteCarlo,
        direct_solving_worker,
    )
except ImportError:
    None
