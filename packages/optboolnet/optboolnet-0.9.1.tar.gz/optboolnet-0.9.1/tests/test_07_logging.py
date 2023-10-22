import pytest
from optboolnet.instances import load_bn_in_repo, iter_bn_in_repo
from optboolnet.config import (
    SolverConfig,
    BendersConfig,
    LoggingConfig,
)
from optboolnet.algorithm import (
    BendersFixPointControl,
)
from itertools import product
import os, sys

stdout_copy = 0
os.dup2(sys.stdout.fileno(), stdout_copy)

# Restore stdout
sys.stdout = os.fdopen(stdout_copy, "w")

_solver_config = SolverConfig(
    {
        "solver_name": "gurobi_persistent",
        "save_results": False,
        "tee": False,
        "warmstart": False,
        "mip_display": 0,
        "threads": 1,
        "timelimit": None,
    }
)


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_logging_1():
    _logging_config = LoggingConfig({"to_stream": False, "fpath": "","fname": ""})
    _benders_config = BendersConfig(
        {
            "enforce": False,
            "max_control_size": 1,
            "max_length": 1,
            "allow_empty_attractor": False,
            "master_solver_config": _solver_config,
            "LLP_solver_config": _solver_config,
            "separation_solver_config": _solver_config,
            "logging_config": _logging_config,
            "solve_separation": False,
            "preprocess_max_forbidden_trap_space": False,
            "separation_heuristic": False,
            "use_high_point_relaxation": True,
            "total_time_limit": None,
        }
    )
    inst = "L1"
    bn = load_bn_in_repo(inst)
    detected = 0
    for _logging_config.fpath, _logging_config.to_stream in product(
        [os.path.dirname(__file__), ""], [True, False]
    ):
        try:
            alg = BendersFixPointControl(inst, bn, _benders_config)
            alg.run_exhaustive_search()
        except NotImplementedError:
            detected += 1
    assert detected == 2


if __name__ == "__main__":
    test_logging_1()
