# ---------- Import Statements (Kapilesh Pennichetty) ----------
from newsapi import NewsApiClient
from flask import Flask, render_template
import datetime

# ---------- API and Program Prerequisites (Kapilesh Pennichetty) ----------
from_date = datetime.date.today() - datetime.timedelta(30)
to_date = datetime.date.today()

# -- News API Prerequisites (Kapilesh Pennichetty) --
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY_HERE')

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
