from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("örnek.html")  # aynı klasördeyse direkt çağırır

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)