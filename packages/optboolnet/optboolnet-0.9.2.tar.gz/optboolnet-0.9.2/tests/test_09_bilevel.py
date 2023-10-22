import os
from optboolnet.mibs import MibSAttractorControl
from optboolnet.instances import load_bn_in_repo, iter_bn_in_repo
from optboolnet.config import MibSBilevelConfig


def test_attractor_control():
    inst = "S4"
    bn = load_bn_in_repo(inst)
    MibS_attr_ctrl = MibSAttractorControl(
        inst,
        bn,
        MibSBilevelConfig(
            {
                "__name__": "MibSBilevelConfig",
                "enforce": True,
                "max_control_size": 3,
                "max_length": 2,
                "allow_empty_attractor": False,
                "use_valid_cuts": True,
                "solver_config": {
                    "__name__": "SolverMibSConfig",
                    "solver_name": "gurobi_persistent",
                    "executable": f"deps\\mibs.exe",
                    "save_results": False,
                    "tee": True,
                    "threads": 1,
                    "warmstart": False,
                    "time_limit": 3,
                },
                "logging_config": {
                    "__name__": "LoggingConfig",
                    "fpath": "tests",
                    "fname": "",
                },
            }
        ),
    )
    MibS_attr_ctrl.run_exhaustive_search()
    print()


if __name__ == "__main__":
    test_attractor_control()
