from ortools.sat.python import cp_model

def bestStaffForTargetByHours():
    # Data
    staffHours = [
        36,
        32,
        40,
        55
    ]

    staffing_target = 3
    num_staff = len(staffHours)

    # Model
    model = cp_model.CpModel()

    print(f'\nStaffing Target {staffing_target}')
    
    # Variables
    x = []
    for i in range(staffing_target):
        t = []
        for j in range(num_staff):
            print(f'Staff {j}.  Hours {staffHours[j]}')
            t.append(model.NewBoolVar(f'x[{i},{j}]'))
        x.append(t)
   
    # Constraints
    # Each staff is assigned to at most one shift.
    for j in range(num_staff):
        model.AddAtMostOne(x[i][j] for i in range(staffing_target))

    # Each task is assigned to exactly one worker.
    for i in range(staffing_target):
        model.AddExactlyOne(x[i][j] for j in range(num_staff))

    # Objectives
    objective_terms = []
    for i in range(staffing_target):
        for j in range(num_staff):
            objective_terms.append(staffHours[j] * x[i][j])

    model.Minimize(sum(objective_terms))
    
    # Solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
        
    # Statistics
    print('\nStatistics')
    print(f'  - status       : {solver.StatusName(status)}')
    print('  - conflicts      : %i' % solver.NumConflicts())
    print('  - branches       : %i' % solver.NumBranches())
    print('  - wall time      : %f s' % solver.WallTime())

    # Solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Total cost = {solver.ObjectiveValue()}')
        print()
        for i in range(staffing_target):
            for j in range(num_staff):
                if solver.BooleanValue(x[i][j]):
                    print(
                        f'Shift {i} assigned to Staff {j}')
    else:
        print('No solution found.')

def main():
    print('ORTools Examples')

    print('\nBest Staff For Staffing Target By Hours')
    bestStaffForTargetByHours()

if __name__ == '__main__':
    main()