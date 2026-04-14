from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from calculator import CalculatorError, evaluate_expression

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/api/calculate")
def calculate():
    payload = request.get_json(silent=True) or {}
    expression = payload.get("expression", "")

    try:
        result = evaluate_expression(expression)
        return jsonify({"result": result}), 200
    except CalculatorError as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
