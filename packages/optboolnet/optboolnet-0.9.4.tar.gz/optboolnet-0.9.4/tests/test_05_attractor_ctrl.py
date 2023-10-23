import pytest
from optboolnet.exception import EmptyAttractorError
from optboolnet.instances import load_bn_in_repo, iter_bn_in_repo
from optboolnet.config import (
    SolverConfig,
    BendersConfig,
    InvalidConfigError,
    LoggingConfig,
)
from optboolnet.algorithm import (
    BendersAttractorControl,
    BendersFixPointControl,
)
from itertools import product
import os, sys

from optboolnet.model import AttractorDetectionIP

stdout_copy = 0
os.dup2(sys.stdout.fileno(), stdout_copy)

# Restore stdout
sys.stdout = os.fdopen(stdout_copy, "w")

_FPATH = os.path.dirname(__file__)


_solver_config = SolverConfig(
    {
        "solver_name": "gurobi_persistent",
        "save_results": False,
        "tee": False,
        "warmstart": False,
        "mip_display": 0,
        "threads": 1,
        "timelimit": 3.0,
    }
)
_logging_config = LoggingConfig(
    {"to_stream": False, "fpath": "", "fname": ""}
)


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_fixed_point_inconsistency():
    _benders_config_dict = {
        "enforce": False,
        "max_control_size": 3,
        "max_length": 1,
        "allow_empty_attractor": False,
        "master_solver_config": _solver_config,
        "LLP_solver_config": _solver_config,
        "separation_solver_config": _solver_config,
        "logging_config": _logging_config,
        "solve_separation": False,  # inconsistent value
        "preprocess_max_forbidden_trap_space": True,
        "separation_heuristic": True,
        "use_high_point_relaxation": True,
        "total_time_limit": None,
    }
    bn = load_bn_in_repo("S1")
    detected = False
    try:
        _incorrect_benders_config = BendersConfig(_benders_config_dict)
        alg = BendersFixPointControl("test", bn, _incorrect_benders_config)
    except InvalidConfigError as e:
        detected = True
        print("Succesfully handled the exception:\n", e)
    assert detected


def test_fixed_point_control():
    _benders_config_dict = {
        "enforce": True,
        "max_control_size": 3,
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

    for (inst, bn), answer in zip(iter_bn_in_repo(["small"]), [12, 5, 0, 9]):
        for [
            _benders_config_dict["use_high_point_relaxation"],
        ] in product([True, False]):
            print(
                inst,
                _benders_config_dict["use_high_point_relaxation"],
            )
            alg = BendersFixPointControl(inst, bn, BendersConfig(_benders_config_dict))
            assert _benders_config_dict["use_high_point_relaxation"] == isinstance(
                alg.model_master, AttractorDetectionIP
            )
            try:
                alg.run_exhaustive_search()
            except EmptyAttractorError:
                continue

            assert alg.solution_count == answer


def test_attractor_control():
    _benders_config_dict = {
        "enforce": False,
        "max_control_size": 2,
        "max_length": 15,
        "allow_empty_attractor": False,
        "master_solver_config": _solver_config,
        "LLP_solver_config": _solver_config,
        "separation_solver_config": _solver_config,
        "logging_config": _logging_config,
        "solve_separation": False,
        "preprocess_max_forbidden_trap_space": False,
        "separation_heuristic": False,
        "use_high_point_relaxation": False,
        "total_time_limit": None,
    }
    for (inst, bn), answer in zip(iter_bn_in_repo(["small"]), [9, 9, 0, 9]):
        print(inst)
        detected = 0
        for (
            _benders_config_dict["solve_separation"],
            _benders_config_dict["preprocess_max_forbidden_trap_space"],
            _benders_config_dict["separation_heuristic"],
        ) in product([True, False], [True, False], [True, False]):
            try:
                alg = BendersAttractorControl(
                    inst, bn, BendersConfig(_benders_config_dict)
                )
                alg.run_exhaustive_search()
                assert alg.solution_count == answer
            except InvalidConfigError:
                detected += 1
        assert detected == 3  # (F,T,T), (F,T,F), (F,F,T)


def test_empty_attractor_detection():
    _logging_config = LoggingConfig(
        {"to_stream": False, "fpath": "", "fname": ""}
    )
    _benders_config = BendersConfig(
        {
            "enforce": False,
            "max_control_size": 1,
            "max_length": 1,
            "master_solver_config": _solver_config,
            "LLP_solver_config": _solver_config,
            "separation_solver_config": _solver_config,
            "logging_config": _logging_config,
            "allow_empty_attractor": False,
            "solve_separation": False,
            "preprocess_max_forbidden_trap_space": False,
            "separation_heuristic": False,
            "use_high_point_relaxation": False,
            "total_time_limit": None,
        }
    )
    inst = "L1"
    bn = load_bn_in_repo(inst)
    detected = False
    try:
        alg = BendersFixPointControl(inst, bn, _benders_config)
        alg.run_exhaustive_search()
    except EmptyAttractorError:
        detected = True
    assert detected


if __name__ == "__main__":
    # test_fixed_point_inconsistency()
    # test_fixed_point_control()
    test_attractor_control()
    # test_empty_attractor_detection()
