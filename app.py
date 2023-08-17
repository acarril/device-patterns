from chalicelib.devices import Pattern
from chalice import Chalice
from fractions import Fraction

app = Chalice(app_name="device_patterns")

def convert2fractions(x):
    return [str(Fraction(i).limit_denominator()) for i in x]

def parse_solutions(solutions: tuple) -> dict:
    sol_min_h_n, sol_min_d = solutions
    return {
        "min_hileras": {
            "densidad": sol_min_h_n[0],
            "patrones": convert2fractions(sol_min_h_n[1])
        },
        "min_densidad": {
            "densidad": sol_min_d[0],
            "patrones": convert2fractions(sol_min_d[1])
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
    solutions = pattern.find_optimal_solutions()
    return parse_solutions(solutions)
