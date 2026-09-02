from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    html_code = """
    <DOCTYPE!html>
    <html>
        <head>
            <title>Merhaba Flask</title>
        </head>
        <body>
            <h1>Dosyasız HTML örneği</h1>
            <p>Bu sayfa Python kodunun içinden geliyor!</p>
        </body>
    </html>
    """
    return render_template_string(html_code)

app.run(host="0.0.0.0", port=5000, debug=True)