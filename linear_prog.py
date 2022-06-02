
from scipy.optimize import linprog
from pprint import pprint

def optimize(objective: list, ineq_matrix: list, ineq_vector: list,
    equal_matrix: list = None, equal_vector: list = None,
    boundaries: list = None, is_minimize: bool = False) -> dict:
    """Use scipy.optimize.linprog to solve the linear programming problem.
    Only minimization optimization is supported and all inequalities must
    have the less or equal to operator.

    The optimization results are returned in a dict containing:
    {Z, xi, xi+1, xi+2, ... , xi+n} where Z is factor being optimized and each
    xi is a variable in the optimization problem
    """

    results = linprog(c=objective, A_ub=ineq_matrix, b_ub=ineq_vector, A_eq=equal_matrix,
    b_eq=equal_vector, bounds=boundaries, method="revised simplex")
    
    to_report = {"Z": results.fun if is_minimize else -results.fun}
    for i in range(len(ineq_matrix[0])):
        to_report[f"x{i+1}"] = results.x[i]

    return to_report

def __do_splitting__(text: str) -> list:
    try:
        vals = [float(i) for i in text.split(",")]
    except ValueError:
        vals = [float(i) for i in text.split()]
    
    return vals

def __collect_rows__(put_here: list):
    while True:
        text = input(f"Enter row{len(put_here)+1} OR q if finished: ")
        if text == 'q':
            break
        put_here.append(__do_splitting__(text))
    
def get_optimization_problem():
    text = input("Enter 1 if your problem is minimization or 2 if maximization: ")
    is_min = True if int(text) == 1 else False
    text = input("Enter optimization coefficients: ")
    obj = __do_splitting__(text)
    if not is_min:
        obj = [-i for i in obj]
    print("Enter the rows of coefficients on left of <= below. Enter q on new line when done.")
    i_matrix = []
    __collect_rows__(i_matrix)
    
    text = input("Enter right hand values of inequalities: ")
    i_vector = __do_splitting__(text)

    text = input("Does your model have equality conditions as well?: 1 = Yes, 2 = No : ")
    eq_matrix = None
    eq_vector = None
    if int(text) == 1:
        print("\nEnter rows on the left of = below. Enter q on line when done.")
        eq_matrix = []
        __collect_rows__(eq_matrix)
        text = input("Enter right hand values of equality conditions: ")
        eq_vector =__do_splitting__(text)

    pprint(optimize(obj, i_matrix, i_vector, is_minimize=is_min, equal_matrix=eq_matrix,
    equal_vector=eq_vector))

if __name__ == "__main__":
    get_optimization_problem()
