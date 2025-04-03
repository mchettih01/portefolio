from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "visits.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"global": 0, "users": {}, "quiz": {}}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visit", methods=["POST"])
def visit():
    user_id = request.json.get("user_id")
    data = load_data()

    data["global"] += 1

    if user_id in data["users"]:
        data["users"][user_id] += 1
    else:
        data["users"][user_id] = 1

    save_data(data)

    return jsonify({
        "global_visits": data["global"],
        "user_visits": data["users"][user_id]
    })

@app.route("/quiz", methods=["POST"])
def quiz():
    answer = request.json.get("answer")
    data = load_data()

    if answer in data["quiz"]:
        data["quiz"][answer] += 1
    else:
        data["quiz"][answer] = 1

    save_data(data)

    responses = {
        "Je m’ennuyais": "L’ennui mène à des endroits étranges.",
        "Je suis curieux(se)": "La curiosité est un vilain défaut.",
        "Je te stalke, j’avoue": "Au moins t’es honnête.",
        "Je voulais voir si t’avais mis quelque chose": "Y’a pas grand chose, mais t’es là.",
        "J’espérais trouver un message": "Tu sais que tu peux m’en envoyer un, non ?",
        "Je ne sais même pas pourquoi je suis là": "Parfois c’est l’univers qui clique pour nous."
    }

    return jsonify({"response": responses.get(answer, "Merci pour ta réponse.")})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
