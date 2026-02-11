from flask import render_template # Remove: import Flask3
import config
from models import Trail
from locations import create, read_one, update, delete
from trails import validate_auth, read_all, create, read_one, update, delete

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    trails = Trail.query.all()
    return render_template("home.html", trails = trails)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)