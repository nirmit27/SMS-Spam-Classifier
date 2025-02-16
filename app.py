from pickle import load
from flask import Flask, jsonify, request, url_for, render_template

app = Flask(__name__)
model = load(open(r'rfc-model.pkl', 'rb'))
vectorizer = load(open(r'tfidf-vectorizer.pkl', 'rb'))


def fetch_label(data: str) -> str:
    """Returns the classification **label** for the message."""
    vector = vectorizer.transform([data]).toarray()
    prediction = model.predict(vector.reshape(1, -1))[0]
    return "HAM" if prediction == 0 else "SPAM"


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html', title="Home")


@app.route("/result", methods=["POST"])
def result():
    user_input = request.form.get('input-area') or ""
    sms = user_input.strip()
    label = fetch_label(sms) if sms != "" else "SPAM"
    color = "red" if label == "SPAM" else "green"
    return render_template('result.html', sms=sms.strip(), label=label, title="Result", color=color)


@app.route("/api/label", methods=["POST"])
def message_label():
    data = request.get_json()
    if 'message' in data.keys():
        message = data['message'].strip()
        data.update({"message": message, "label": fetch_label(message)
                    if message != "" else "SPAM"})
        return jsonify(data), 200

    return jsonify({"error": "Invalid input"}), 404


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error.description, title="Not Found")


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=error.description, title="Internal Server Error")


if __name__ == "__main__":
    with app.app_context():
        app.run(port=5000)
