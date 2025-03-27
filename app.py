from flask import Flask, request, jsonify
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import math

app = Flask(__name__)

# Commonly used symbols
x, y, z, a, b, c, r, theta, n = symbols('x y z a b c r theta n')

@app.route("/")
def home():
    return "SymPy Olympiad API is live!"

# --- Algebra ---
@app.route("/algebra/solve", methods=["POST"])
def solve_equation():
    data = request.json
    expr = parse_expr(data["expression"])
    variable = symbols(data.get("variable", "x"))
    sol = solve(expr, variable)
    return jsonify({"solutions": [str(s) for s in sol]})

@app.route("/algebra/simplify", methods=["POST"])
def simplify_expression():
    data = request.json
    expr = parse_expr(data["expression"])
    result = simplify(expr)
    return jsonify({"result": str(result)})

# --- Geometry ---
@app.route("/geometry/plane", methods=["POST"])
def solve_plane_geometry():
    data = request.json
    expr = parse_expr(data["expression"])
    result = simplify(expr)
    return jsonify({"result": str(result)})

@app.route("/geometry/solid", methods=["POST"])
def solve_solid_geometry():
    data = request.json
    expr = data["expression"]
    parts = expr.split(";")

    try:
        main_expr = parse_expr(parts[0].split("=")[1].strip())
        subs = {}
        for part in parts[1:]:
            if "=" in part:
                k, v = part.strip().split("=")
                subs[symbols(k.strip())] = float(v)
        result = main_expr.subs(subs).evalf()
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- Combinatorics ---
@app.route("/combinatorics", methods=["POST"])
def combinatorics_solve():
    data = request.json
    try:
        expr = parse_expr(data["expression"], evaluate=False)
        result = expr.evalf()
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- Number Theory ---
@app.route("/number-theory", methods=["POST"])
def number_theory_tools():
    data = request.json
    try:
        expr = parse_expr(data["expression"])
        result = expr.evalf()
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- Olympiad Advanced Multi-Step Reasoning ---
@app.route("/olympiad/advanced", methods=["POST"])
def solve_olympiad_problem():
    data = request.json
    current_expr = None

    try:
        for step in data["steps"]:
            op = step["operation"]
            expr = step.get("expression", "")
            variable = step.get("variable", "x")
            substitutions = step.get("substitutions", {})

            if expr:
                current_expr = parse_expr(expr)

            if op == "simplify":
                current_expr = simplify(current_expr)
            elif op == "solve":
                current_expr = solve(current_expr, symbols(variable))
            elif op == "substitute":
                subs = {symbols(k): parse_expr(v) for k, v in substitutions.items()}
                current_expr = current_expr.subs(subs)
            elif op == "expand":
                current_expr = expand(current_expr)
            elif op == "factor":
                current_expr = factor(current_expr)
            elif op == "differentiate":
                current_expr = diff(current_expr, symbols(variable))
            elif op == "integrate":
                current_expr = integrate(current_expr, symbols(variable))
            else:
                return jsonify({"error": f"Unknown operation: {op}"}), 400

        return jsonify({"result": str(current_expr)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
