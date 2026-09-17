import json
from flask import Flask, render_template, abort, Response
from datetime import datetime

app = Flask(__name__)

with open("data/laws.json") as f:
    laws = json.load(f)

with open("data/glossary.json") as f:
    glossary = json.load(f)

with open("data/explainers.json") as f:
    explainers = json.load(f)

def make_slug(name):
    return name.lower().replace(" ", "-").replace(",", "")

for law in laws:
    law["slug"] = make_slug(law["name"])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/laws")
def laws_list():
    return render_template("laws_index.html", laws=laws)

@app.route("/laws/<slug>")
def law_detail(slug):
    for law in laws:
        if law["slug"] == slug:
            return render_template("law_detail.html", law=law)
    abort(404)

@app.route("/glossary")
def glossary_list():
    return render_template("glossary.html", glossary=glossary)

@app.route("/explainers")
def explainers_list():
    return render_template("explainers_index.html", explainers=explainers)

@app.route("/explainers/<slug>")
def explainer_detail(slug):
    for explainer in explainers:
        if explainer["slug"] == slug:
            return render_template("explainers_detail.html", explainer=explainer)
    abort(404)
    
# Date in footer
@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

# Creates the sitemap.xml file for search engines - keeps it fresh
@app.route("/sitemap.xml")
def sitemap():
    pages = ["", "/laws", "/glossary", "/explainers"]
    pages += [f"/laws/{law['slug']}" for law in laws]
    pages += [f"/explainers/{e['slug']}" for e in explainers]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in pages:
        xml.append(f"<url><loc>https://rugbylaws.co.za{page}</loc></url>")
    xml.append("</urlset>")

    return Response("\n".join(xml), mimetype="application/xml")

# tells search engine crawlers (Googlebot, Bingbot, etc.) which parts of your site they're allowed to crawl and index, and optionally points them to your sitemap.
@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

@app.route("/ads.txt")
def ads():
    return app.send_static_file("ads.txt")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)