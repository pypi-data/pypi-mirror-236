import sys, os
from typing import Iterator
import pyomo.environ as pe
from pao.pyomo import *
import pao
import pao.common

from optboolnet.config import SolverConfig


class PrintIter(Iterator):
    def __init__(self, old_iter):
        self.old_iter = old_iter

    def __next__(self):
        value = next(self.old_iter, None)
        if value == None:
            raise StopIteration()
        else:
            print(value)
            return value


def test_single_lower_level():
    # Create a model object
    M = pe.ConcreteModel()

    # Define decision variables
    M.x = pe.Var(bounds=(0, None), domain=pe.Integers)
    M.y = pe.Var(bounds=(0, None), domain=pe.Integers)

    # Define the upper-level objective
    M.o = pe.Objective(expr=M.x - 4 * M.y)

    # Create a SubModel component to declare a lower-level problem
    # The variable M.x is fixed in this lower-level problem
    M.L = SubModel(fixed=M.x)

    # Define the lower-level objective
    M.L.o = pe.Objective(expr=M.y)

    # Define lower-level constraints
    M.L.c1 = pe.Constraint(expr=-M.x - M.y <= -3)
    M.L.c2 = pe.Constraint(expr=-2 * M.x + M.y <= 0)
    M.L.c3 = pe.Constraint(expr=2 * M.x + M.y <= 12)
    M.L.c4 = pe.Constraint(expr=3 * M.x - 2 * M.y <= 4)

    # Create a solver and apply it
    _mip_solver = Solver("gurobi")
    with Solver("pao.pyomo.FA", mip_solver=_mip_solver) as solver:
        results = solver.solve(M)

    # The final solution is loaded into the model
    print(M.x.value)
    print(M.y.value)


def test_single_lower_level_mibs():
    # Create a model object
    M = pe.ConcreteModel()

    # Define decision variables
    M.x = pe.Var(bounds=(0, None), domain=pe.Integers)
    M.y = pe.Var(bounds=(0, None), domain=pe.Integers)

    # Define the upper-level objective
    M.o = pe.Objective(expr=M.x - 4 * M.y)

    # Create a SubModel component to declare a lower-level problem
    # The variable M.x is fixed in this lower-level problem
    M.L = SubModel(fixed=M.x)

    # Define the lower-level objective
    M.L.o = pe.Objective(expr=M.y)

    # Define lower-level constraints
    M.L.c1 = pe.Constraint(expr=-M.x - M.y <= -3)
    M.L.c2 = pe.Constraint(expr=-2 * M.x + M.y <= 0)
    M.L.c3 = pe.Constraint(expr=2 * M.x + M.y <= 12)
    M.L.c4 = pe.Constraint(expr=3 * M.x - 2 * M.y <= 4)

    solve_by_mibs(M, "deps\\mibs\\mibs.exe")

    # Create a solver and apply it
    # with Solver("pao.pyomo.MIBS") as solver:
    #     results = solver.solve(M)
    # solver.

    # The final solution is loaded into the model
    print(M.x.value)
    print(M.y.value)


def test_multiple_lower_level():
    M = pe.ConcreteModel()

    M.x = pe.Var(bounds=(2, 6))
    # M.x = pe.Var(bounds=(2, 6), domain=pe.Integers)
    # M.y = pe.Var()
    # M.z = pe.Var([1, 2], bounds=(0, None), domain=pe.Integers)
    M.z = pe.Var([1, 2], bounds=(0, None))

    M.o = pe.Objective(expr=M.x + 3 * M.z[1] + 3 * M.z[2], sense=pe.minimize)
    # M.c = pe.Constraint(expr=M.x + M.y == 10)

    M.L1 = SubModel(fixed=[M.x])
    M.L1.o = pe.Objective(expr=M.z[1], sense=pe.maximize)
    M.L1.c1 = pe.Constraint(expr=M.x + M.z[1] <= 8)
    M.L1.c2 = pe.Constraint(expr=M.x + 4 * M.z[1] >= 8)
    M.L1.c3 = pe.Constraint(expr=M.x + 2 * M.z[1] <= 13)

    # M.L2 = SubModel(fixed=[M.y])
    # M.L1.o = pe.Objective(expr=M.z[2], sense=pe.maximize)
    # M.L1.c1 = pe.Constraint(expr=M.y + M.z[2] <= 8)
    # M.L1.c2 = pe.Constraint(expr=M.y + 4 * M.z[2] >= 8)
    # M.L1.c3 = pe.Constraint(expr=M.y + 2 * M.z[2] <= 13)

    # opt = pao.Solver("pao.pyomo.MIBS")

    _mip_solver = Solver("gurobi")
    opt = pao.Solver("pao.pyomo.FA", mip_solver=_mip_solver)
    results = opt.solve(M)

    # solve_by_mibs(M, "deps\\mibs\\mibs.exe")
    print(M.x.value, M.z[1].value, M.z[2].value)
    # print(M.x.value, M.y.value, M.z[1].value, M.z[2].value)


def test_mibs_interface():
    # Create a model object
    M = pe.ConcreteModel()

    # Define decision variables
    # M.x = pe.Var(bounds=(0, 10))
    # M.y = pe.Var(bounds=(0, None))
    # M.z = pe.Var(bounds=(0, None))
    M.x = pe.Var(bounds=(0, 10), domain=pe.Integers)
    M.y = pe.Var(bounds=(0, None), domain=pe.Integers)
    M.z = pe.Var(bounds=(0, None), domain=pe.Integers)

    # Define the upper-level objective
    M.o = pe.Objective(expr=-M.x - 7 * M.z)
    M.cu1 = pe.Constraint(expr=-3 * M.x + 2 * M.y <= 12)
    M.cu2 = pe.Constraint(expr=M.x + 2 * M.y <= 20)

    # Create a SubModel component to declare a lower-level problem
    # The variable M.x is fixed in this lower-level problem
    M.L = SubModel(fixed=M.x)

    # Define the lower-level objective
    M.L.o = pe.Objective(expr=M.z)

    # Define lower-level constraints
    M.L.c1 = pe.Constraint(expr=2 * M.x - M.z <= 7)
    M.L.c2 = pe.Constraint(expr=-2 * M.x + 4 * M.y <= 16)
    M.L.c3 = pe.Constraint(expr=M.z <= 5)
    # Create a solver and apply it

    solve_by_mibs(M, "deps\\mibs\\mibs.exe")
    print(M.x.value)
    print(M.y.value)
    print(M.z.value)
    # _mip_solver = Solver("gurobi")
    # opt = pao.Solver("pao.pyomo.FA", mip_solver=_mip_solver)
    # results = opt.solve(M)
    # print(M.x.value, M.y.value, M.z.value)


def test_MibS_attractor_control():
    from optboolnet.mibs import MibSBilevelIP
    from optboolnet.instances import load_bn_in_repo

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
    bn = load_bn_in_repo("M1")
    bilevel_model = MibSBilevelIP("MibS_test", bn, 1, _solver_config)
    # bilevel_model.add_valid_cut()
    for target_size in range(8):
        print(target_size)
        bilevel_model.set_constr_target_size(target_size)
        while solve_by_mibs(bilevel_model, "deps\\mibs\\mibs.exe"):
            ctrl = bilevel_model.get_control()
            print(ctrl)
            bilevel_model.append_minimality_cut(ctrl)
    # solve_by_mibs(bilevel_model, "deps\\mibs\\mibs.exe")
    # ctrl = bilevel_model.get_control()

    # print(ctrl)
    # bilevel_model.pprint()


if __name__ == "__main__":
    # test_single_lower_level_mibs()
    # test_multiple_lower_level()
    # test_mibs_interface()
    test_MibS_attractor_control()
