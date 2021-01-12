# ---------- Import Statements (Kapilesh Pennichetty) ----------
from newsapi import NewsApiClient
from flask import Flask, render_template
import datetime

# ---------- Sources ----------
"""
- Flask PWA Developement Process: https://www.flaskpwa.com/
Helped in the process of learning to develop a Progressive Web App using the Flask framework. The file at static/manifest.json was derived from the manifest.json in the website.
- W3 Schools: https://w3schools.com/
Helped in implementing Bootstrap templates and CSS.
- Stack Overflow (Used only for reading through previously asked questions): https://stackoverflow.com
Helped in learning how to passing data from Python to HTML page: 
https://stackoverflow.com/questions/51669102/how-to-pass-data-to-html-page-using-flask 
- Flask Documentation: 
https://flask.palletsprojects.com/en/1.1.x/
Helped in the process of learning the Flask Web Development Framework.
-  Jinja Documentation:
https://jinja.palletsprojects.com/en/2.11.x/
Helped in the process of learning how to initiate a 
for-each loop for html attributes, and learning how to access Python functions through HTML.
- How to code a WEB APP using Flask (Flask Python Tutorial for Beginners) ft ~*doggo roulette*~ by Kylie Ying:
https://youtu.be/8q3qje9K5uU
Helped in the process of learning how to use Flask to develop webpages and web-based applications.
- Flask Tutorial #1 - How to Make Websites with Python by Tech with Tim:
https://youtu.be/mqhxxeeTbu0
Helped in the process of learning the basics of Flask.
- Python Library for News API: https://github.com/mattlisiv/newsapi-python
Helped implement the News API in the Progressive Web App.
- Documentation for News API: https://newsapi.org/docs
Helped in the process of learning the functions, inputs, and outputs of the News API.
"""

# ---------- API and Program Prerequisites (Kapilesh Pennichetty) ----------
from_date = datetime.date.today() - datetime.timedelta(30)
to_date = datetime.date.today()

# -- News API Prerequisites (Kapilesh Pennichetty) --
newsapi = NewsApiClient(api_key='eadbfa9229d14334b96c95ccd2d733e1')

# -- Flask Framework Initialization (Kapilesh Pennichetty) --
app = Flask(__name__)

# ---------- Defining Functions and Variables (Kapilesh Pennichetty) ----------
stats = newsapi.get_everything(
    q='top-headlines',
    from_param=from_date,
    to=to_date,
    sort_by='publishedAt',
    language='en')
all_articles = stats["articles"]


# ----- Webpages (Kapilesh Pennichetty) -----
# -- Home Page (Kapilesh Pennichetty) --
@app.route("/")
def home():
    return render_template('main.html', all_articles=all_articles)


# ---------- Initializing Flask App (Kapilesh Pennichetty) ----------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)