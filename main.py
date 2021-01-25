# ---------- Import Statements ----------
from threading import Thread
from time import sleep
from flask import Flask, render_template
from newsapi import NewsApiClient


# ---------- API and Program Prerequisites (Kapilesh Pennichetty) ----------

# -- News API Prerequisites (Kapilesh Pennichetty) --
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY_HERE')  # Registering API Key for Use and Abstracting
# Key Away (Source: https://newsapi.org/docs)

# -- Flask Framework Prerequisites (Kapilesh Pennichetty) --
app = Flask(__name__)  # Source: https://flask.palletsprojects.com/en/1.1.x/


# ---------- Collection Types and Function Definitions ----------

# ----- List and Format Trusted News Sources (Kapilesh Pennichetty) -----
trusted_news_sources = [
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


def format_trusted_news_sources():
    """Formats the trusted_news_sources list for use with the News API."""
    news_outlets = ""  # Blank string to append as needed using for-each loop.
    for source in trusted_news_sources:
        source += ","  # Adding a comma to separate the news sources as per the API format.
        news_outlets += source  # Appending newly formatted news sources to a variable news_outlets to be fed into
        # the API.
    trusted_news = news_outlets[
                   0:-1]  # Removing the comma from the last news source.
    return trusted_news


# ----- Fetching and Filtering Article Data (Kapilesh Pennichetty) -----

def get_top_headlines_stats():
    """Fetches Article Data and Metadata from the API (Source: https://newsapi.org/docs)"""
    top_headlines_stats = newsapi.get_top_headlines(  # Requesting data from the News API about the top headlines
        sources=format_trusted_news_sources(),
        language='en')
    return top_headlines_stats


def separate_top_articles_stats():
    """Filters out article data from API metadata"""
    top_headlines_stats = get_top_headlines_stats()
    all_top_articles = top_headlines_stats[
        "articles"]  # Separating articles from the search query data
    return all_top_articles


def repeat_top_headlines():
    """This function runs an infinite loop to fetch top headlines every 30 minutes"""
    global top_headlines
    top_headlines = separate_top_articles_stats()
    while True:
        sleep(1800)  # 1800 Seconds = 30 Minutes
        top_headlines = separate_top_articles_stats()


# ----- Webpages (Source: https://flask.palletsprojects.com/en/1.1.x/ and
# https://jinja.palletsprojects.com/en/2.11.x/) -----

# -- Home Page (Kapilesh Pennichetty) --
@app.route("/")  # Telling Flask that the url with "/" appended at the end should lead to the home page.
def home():
    """Home page that shows trending articles."""
    return render_template('home.html', top_articles=top_headlines)
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.


# ---------- Main Code ----------

# ----- Run repeat_top_headlines() in a background thread (Kapilesh Pennichetty) -----
fetch_articles = Thread(name='background', target=repeat_top_headlines)
fetch_articles.daemon = True
fetch_articles.start()

# ----- Run Flask App (Kapilesh Pennichetty) -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # Telling Flask to run the app with the constraints given. (Source:
    # https://flask.palletsprojects.com/en/1.1.x/)
