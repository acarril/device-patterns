from chalicelib.devices import Pattern
from chalice import Chalice
from fractions import Fraction

app = Chalice(app_name="device_patterns")

def distribute_patterns(patterns):
    f = lambda m, n: [i*n//m + n//(2*m) for i in range(m)]
    non_zeros = [p for p in patterns if p != "0"]
    non_zero_indices =  f(len(non_zeros), len(patterns))
    result = ["0"] * len(patterns)
    for i, p in zip(non_zero_indices, non_zeros):
        result[i] = p
    return result

def process_solution_patterns(patterns:list) -> list:
    """Process solution patterns to return them in a sorted list of string fractions."""
    frac_patterns = sorted([Fraction(pat).limit_denominator() for pat in patterns], reverse=True)
    str_patterns = [str(pat) for pat in frac_patterns]
    return distribute_patterns(str_patterns)

def parse_solutions(optimal_solution: tuple) -> dict:
    # Unpack objects in optimal solution
    computed_d, solution_pattern, criterion = optimal_solution
    # Return parsed solution as JSON/dictionary
    return {
            "densidad": computed_d,
            "patrones": process_solution_patterns(solution_pattern),
            "criterio": criterion
    }

@app.route("/hello",  methods=['GET'], cors=True)
def index():
    return {"nikito": "time"}

@app.route('/', methods=['POST'], cors=True)
def get_solutions():
    # Fetch query params
    req_body = app.current_request.json_body
    # Instantiate Pattern class
    pattern = Pattern(**req_body)
    # Find optimal solutions
    optimal_solution = pattern.run()
    # Check solutions and parse them accordingly
    if optimal_solution is None:
        return None
    else:
        return parse_solutions(optimal_solution)
