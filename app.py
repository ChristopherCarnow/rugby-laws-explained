import json
from flask import Flask, render_template, abort

app = Flask(__name__)

with open("data/laws.json") as f:
    laws = json.load(f)

def make_slug(name):
    return name.lower().replace(" ", "-").replace(",", "")

# Add a slug to each law, once, at startup
for law in laws:
    law["slug"] = make_slug(law["name"])

@app.route("/")
def home():
    return render_template("laws_index.html", laws=laws)

@app.route("/laws")
def laws_list():
    return render_template("laws_index.html", laws=laws)

@app.route("/laws/<slug>")
def law_detail(slug):
    for law in laws:
        if law["slug"] == slug:
            return render_template("law_detail.html", law=law)
    abort(404)

if __name__ == "__main__":
    app.run(debug=True, port=5001)