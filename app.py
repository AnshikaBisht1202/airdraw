from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json

    print(data.keys())

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)