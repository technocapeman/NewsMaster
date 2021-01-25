# ---------- Import Statements ----------
from threading import Thread
from time import sleep

import requests
from flask import Flask, render_template


# ---------- API and Program Prerequisites (Kapilesh Pennichetty) ----------

api_key = 'YOUR_NEWSAPI_KEY_HERE'  # Defining API Key for use with News API

app = Flask(__name__)  # Defining Flask App (Source: https://flask.palletsprojects.com/en/1.1.x/)


# ---------- Collection Types and Function Definitions ----------

# ----- List and Format Trusted News Sources (Kapilesh Pennichetty) -----
trusted_news_sources_list = [
    "bbc-news", "abc-news", "abc-news-au", "al-jazeera-english",
    "ars-technica", "associated-press", "australian-financial-review", "axios",
    "bbc-sport", "bleacher-report", "bloomberg", "breitbart-news",
    "business-insider", "cbc-news", "cbs-news", "cnn", "crypto-coins-news",
    "engadget", "espn", "financial-post", "football-italia",
    "fortune", "four-four-two", "fox-news", "fox-sports",
    "google-news", "google-news-au", "google-news-ca", "google-news-in",
    "google-news-uk", "independent", "mashable", "medical-news-today",
    "msnbc", "mtv-news", "mtv-news-uk", "national-geographic",
    "national-review", "nbc-news", "new-scientist", "news-com-au", "newsweek",
    "new-york-magazine", "nfl-news", "nhl-news", "politico", "polygon",
    "recode", "reuters", "rte", "talksport", "techcrunch", "techradar",
    "the-globe-and-mail", "the-hill", "the-hindu", "the-huffington-post",
    "the-irish-times", "the-jerusalem-post", "the-next-web",
    "the-times-of-india", "the-verge", "the-wall-street-journal",
    "the-washington-post", "the-washington-times", "time", "usa-today",
    "vice-news", "wired"
]

trusted_news_sources = ",".join(trusted_news_sources_list)  # Formatting list for use with API


# ----- Fetching and Filtering Article Data (Kapilesh Pennichetty) -----

def get_top_headlines_stats():
    """Fetches Article Data and Metadata from the API (Documentation:
    https://newsapi.org/docs/endpoints/top-headlines) """
    url = f'http://newsapi.org/v2/top-headlines?' \
          f'sources={trusted_news_sources}&' \
          f'apiKey={api_key}'
    api_output = requests.get(url)
    top_headlines_stats = api_output.json()
    return top_headlines_stats["articles"]


def fetch_top_headlines():
    """This function runs an infinite loop to fetch top headlines every 30 minutes"""
    global top_headlines
    top_headlines = get_top_headlines_stats()
    while True:
        sleep(30*60)  # 30 mins x 60 secs per min = 1800 seconds
        top_headlines = get_top_headlines_stats()


# ----- Webpages (Documentation: https://flask.palletsprojects.com/en/1.1.x/ and
# https://jinja.palletsprojects.com/en/2.11.x/) -----

# -- Home Page (Kapilesh Pennichetty) --
@app.route("/")  # Telling Flask that the url with "/" appended at the end should lead to the home page.
def home():
    """Home page that shows trending articles."""
    return render_template('home.html', top_articles=top_headlines)
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.


# ---------- Main Code ----------

# ----- Run repeat_top_headlines() in a background thread (Kapilesh Pennichetty) -----
# Reference: https://stackoverflow.com/questions/38254172/infinite-while-true-loop-in-the-background-python
fetch_articles = Thread(name='background', target=fetch_top_headlines)
fetch_articles.daemon = True
fetch_articles.start()

# ----- Run Flask App (Kapilesh Pennichetty) -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # Telling Flask to run the app with the constraints given. (Documentation:
    # https://flask.palletsprojects.com/en/1.1.x/)
