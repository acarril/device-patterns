from chalicelib.devices import Pattern
from chalice import Chalice
from fractions import Fraction

app = Chalice(app_name="device_patterns")

def convert2fractions(x):
    return [str(Fraction(i).limit_denominator()) for i in x]

def parse_solutions(optimal_solution: tuple) -> dict:
    # Unpack objects in optimal solution
    computed_d, solution_pattern, criterion = optimal_solution
    # Return parsed solution as JSON/dictionary
    return {
        criterion: {
            "densidad": computed_d,
            "patrones": convert2fractions(solution_pattern)
        }
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
