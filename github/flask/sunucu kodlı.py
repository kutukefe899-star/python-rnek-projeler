from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gelişmiş Hesap Makinesi</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="calculator">
    <div class="display" id="display">0</div>
    <div class="buttons">
      <button class="btn" data-action="clear">C</button>
      <button class="btn" data-action="back">⌫</button>
      <button class="btn" data-action="percent">%</button>
      <button class="btn operator" data-action="/">÷</button>

      <button class="btn" data-action="7">7</button>
      <button class="btn" data-action="8">8</button>
      <button class="btn" data-action="9">9</button>
      <button class="btn operator" data-action="*">×</button>

      <button class="btn" data-action="4">4</button>
      <button class="btn" data-action="5">5</button>
      <button class="btn" data-action="6">6</button>
      <button class="btn operator" data-action="-">−</button>

      <button class="btn" data-action="1">1</button>
      <button class="btn" data-action="2">2</button>
      <button class="btn" data-action="3">3</button>
      <button class="btn operator" data-action="+">+</button>

      <button class="btn" data-action="0">0</button>
      <button class="btn" data-action=".">.</button>
      <button class="btn equal" data-action="=">=</button>
    </div>
  </div>
  <script src="script.js"></script>
</body>
</html><style>body {
  background: linear-gradient(135deg, #1f1c2c, #928dab);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
}

.calculator {
  background: #2c2c2c;
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.5);
  padding: 20px;
  width: 320px;
}

.display {
  background: #111;
  color: #0f0;
  font-size: 2em;
  text-align: right;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: inset 0 0 10px #000;
}

.buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.btn {
  background: linear-gradient(145deg, #3a3a3a, #1a1a1a);
  border: none;
  border-radius: 12px;
  padding: 20px;
  font-size: 1.2em;
  color: #fff;
  box-shadow: 5px 5px 10px #000, -5px -5px 10px #444;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:active {
  transform: translateY(3px);
  box-shadow: inset 3px 3px 6px #000, inset -3px -3px 6px #444;
}

.operator {
  background: linear-gradient(145deg, #ff6a00, #ff3c00);
}

.equal {
  grid-column: span 2;
  background: linear-gradient(145deg, #00c6ff, #0072ff);
}</style><script>const display = document.getElementById("display");
const buttons = document.querySelectorAll(".btn");

let currentInput = "";
let resetNext = false;

buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    const action = btn.getAttribute("data-action");

    if (action === "clear") {
      currentInput = "";
      display.textContent = "0";
    } else if (action === "back") {
      currentInput = currentInput.slice(0, -1);
      display.textContent = currentInput || "0";
    } else if (action === "=") {
      try {
        currentInput = eval(currentInput).toString();
        display.textContent = currentInput;
        resetNext = true;
      } catch {
        display.textContent = "Error";
        currentInput = "";
      }
    } else if (action === "percent") {
      currentInput = (parseFloat(currentInput) / 100).toString();
      display.textContent = currentInput;
    } else {
      if (resetNext) {
        currentInput = "";
        resetNext = false;
      }
      currentInput += action;
      display.textContent = currentInput;
    }
  });
});</script>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)