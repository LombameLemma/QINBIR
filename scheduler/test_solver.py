from ortools.sat.python import cp_model


def main():
    model = cp_model.CpModel()

    x = model.NewBoolVar("x")

    model.Add(x == 1)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    print("Solver status:", solver.StatusName(status))
    print("x =", solver.Value(x))


if __name__ == "__main__":
    main()