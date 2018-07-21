from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/raleigh_craigslist_db"
mongo = PyMongo(app)

@app.route("/")
def home():
    data = mongo.db.mars_results.find_one()
    return render_template("index.html", data=data)

@app.route("/scrape")
def scrape():
    mars_results = mongo.db.mars_results
    data = scrape_mars.scrape()
    mars_results.update(
        {},
        data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)