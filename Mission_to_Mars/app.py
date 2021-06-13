from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection 
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config['MONGO_URI'] = "mongodb://localhost:27017/marsdata_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars_dict = mongo.db.marsdata.find_one()
    return render_template("index.html", mars_dict=mars_dict)
    


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    #run scrape function
    mars_dict = scrape_mars.scrape_info()
    
    #update the Mongo database
    mongo.db.marsdata.update({}, mars_dict, upsert=True)

    #redirect back to homepage
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)