from pickle import load
from flask import Flask, jsonify, request, url_for, render_template

app = Flask(__name__)
model = load(open(r'rfc-model.pkl', 'rb'))
vectorizer = load(open(r'tfidf-vectorizer.pkl', 'rb'))


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html', title="SMS Classifier")


@app.route("/api/label", methods=["POST"])
def message_label():
    data = request.get_json()
    vector = vectorizer.transform([data['message']]).toarray()
    prediction = model.predict(vector.reshape(1, -1))[0]

    data.update({"label": "HAM" if prediction == 0 else "SPAM"})
    return jsonify(data), 200


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error.description, title="Not Found")


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=error.description, title="Internal Server Error")


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, port=5000)
