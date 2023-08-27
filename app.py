from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from pymongo import MongoClient

app = Flask(__name__)
Bootstrap(app)

# Configuration de la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Scraping"]
collection = db["data"]


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form.get("query")
        results_cursor = collection.find(
            {"Contenus": {"$regex": query, "$options": "i"}}
        )
        for result in results_cursor:
            title = result.get("Titre", "Titre")
            content = result.get("Contenus", "Contenu")
            content_preview = content[:500] + "..." if len(content) > 500 else content
            formatted_result = {"titre": title, "contenu": content_preview}
            results.append(formatted_result)
    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
