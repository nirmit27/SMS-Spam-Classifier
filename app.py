from flask import Flask, jsonify, render_template, request, url_for

app: Flask = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html', title='Home')


@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
