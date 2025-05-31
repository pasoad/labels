from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Dossier des entêtes
HEADER_FOLDER = os.path.join("static", "headers")
os.makedirs(HEADER_FOLDER, exist_ok=True)
app.config['HEADER_FOLDER'] = HEADER_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    headers = os.listdir(HEADER_FOLDER)
    if request.method == "POST":
        article = request.form.get("article")
        prix = float(request.form.get("prix", 0))
        accessoires = request.form.get("accessoires")
        entete = request.form.get("entete")

        accessoires_list = [x.strip() for x in accessoires.split(",") if x.strip()] if accessoires else []
        total = prix + sum([5.0 for _ in accessoires_list])  # Exemple: chaque accessoire ajoute 5€

        return render_template("preview.html", article=article, prix=prix, accessoires=accessoires_list, entete=entete, total=total)

    return render_template("index.html", headers=headers)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename != "":
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['HEADER_FOLDER'], filename))

    return redirect(url_for("index"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

