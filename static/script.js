const expressionInput = document.getElementById("expression");
const resultEl = document.getElementById("result");

async function calculate() {
  const expression = expressionInput.value;
  if (!expression.trim()) {
    resultEl.textContent = "Result: Enter an expression.";
    return;
  }

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression }),
    });

    const payload = await response.json();

    if (!response.ok) {
      resultEl.textContent = `Result: ${payload.error || "Failed to calculate."}`;
      return;
    }

    resultEl.textContent = `Result: ${payload.result}`;
  } catch (error) {
    resultEl.textContent = "Result: Service is unavailable.";
  }
}

for (const button of document.querySelectorAll("button[data-value]")) {
  button.addEventListener("click", () => {
    expressionInput.value += button.dataset.value;
    expressionInput.focus();
  });
}

document.getElementById("clear").addEventListener("click", () => {
  expressionInput.value = "";
  resultEl.textContent = "Result: -";
  expressionInput.focus();
});

document.getElementById("calculate").addEventListener("click", calculate);
expressionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    calculate();
  }
});
