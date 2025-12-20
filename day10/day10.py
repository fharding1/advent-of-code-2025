from z3 import *

with open('input', 'r') as file:
    acc = 0
    for line in file:
        processed_line = line.strip().split(' ')
        goal = []
        for ch in processed_line[0][1:len(processed_line[0])-1]:
            if ch == '.':
                goal.append(0)
            else:
                goal.append(1)
        
        buttons = []
        for raw_button in processed_line[1:len(processed_line)-1]:
            buttons.append([int(x) for x in raw_button.strip('()').split(',')])

        goal_joltages = [int(x) for x in processed_line[-1].strip('{}').split(',')]

        # print(goal_joltages)

        # Create variables
        vars = [Int('a' + str(i)) for i in range(len(buttons))]

        # Create solver
        s = Solver()

        # Add constraints
        for var in vars:
            s.add(var >= 0)

        for i in range(len(goal)):
            b = goal[i]
            lhs = 0
            for j in range(len(buttons)):
                if i in buttons[j]:
                    lhs += vars[j]
            # print(lhs, b)
            # s.add((lhs) % 2 == b)
            print(lhs,goal_joltages[i])
            s.add(lhs == goal_joltages[i])

        lowest = 999999999

        if s.check() == unsat:
            print('unsat')
            continue

        while s.check() == sat:
            m = s.model()
            res = sum([m.eval(var).as_long() for var in vars])
            lowest = res
            s.add(sum(vars) < lowest)

        print(lowest)
        acc += lowest

        # A = []
        # for i in range(len(b)):
        #     row = []
        #     for button in buttons:
        #         if i in button:
        #             row.append(1)
        #         else:
        #             row.append(0)
        #     for j in range(len(b)):
        #         if i == j:
        #             row.append(-2)
        #         else:
        #             row.append(0)
        #     A.append(row)
        
        # print("A: ", A)
        # print("b: ", b)

        # bounds = ([(0,None)]*(len(A[0])))

        # print("bounds", bounds)

        # n_vars = len(buttons) + len(b)

        # c = np.array([1] * len(buttons) + [0] * len(b))

        # constraints = [
        #     LinearConstraint(A, lb=b, ub=b)
        # ]

        # bounds = Bounds([0]*n_vars, [1]*n_vars)  # or higher if needed

        # integrality = np.ones(n_vars, dtype=int)

        # res = milp(
        #     c=c,
        #     constraints=constraints,
        #     bounds=bounds,
        #     integrality=integrality
        # )

        # print(np.linalg.solve(A,b))

        # print(res)
        # print(res.x[:len(buttons)])
        # acc += sum(res.x[:len(buttons)])
        
        # res = linprog([1] * len(buttons) + [0] * len(A), A_eq=A, b_eq=b, bounds=bounds, method="highs")
    print(acc)
