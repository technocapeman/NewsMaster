# ---------- Import Statements ----------
from threading import Thread
from time import sleep

import requests
import schedule
from flask import Flask, render_template


# ---------- API and Program Prerequisites (Kapilesh Pennichetty) ----------

newsapi_key = 'YOUR_NEWSAPI_KEY_HERE'  # Defining API Key for use with News API

ipstackapi_key = 'YOUR_IPSTACK_API_KEY_HERE'  # Defining API Key for use with IPStack API

app = Flask(__name__)  # Defining Flask App (Source: https://flask.palletsprojects.com/en/1.1.x/)


# ---------- Functions and Data ----------

# ------- Trending News (Kapilesh Pennichetty) -------

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
    https://newsapi.org/docs/endpoints/top-headlines)"""
    url = f'http://newsapi.org/v2/top-headlines?' \
          f'sources={trusted_news_sources}&' \
          f'apiKey={newsapi_key}'
    api_output = requests.get(url)
    top_headlines_stats = api_output.json()
    return top_headlines_stats["articles"]


def fetch_top_headlines():
    """This function runs fetches top headlines when called."""
    global top_headlines
    top_headlines = get_top_headlines_stats()


def background_fetch():
    """This function repeatedly calls fetch_top_headlines() every 30 minutes
     (Documentation: https://schedule.readthedocs.io/en/stable/index.html)."""
    fetch_top_headlines()
    schedule.every(45).minutes.do(fetch_top_headlines)
    while True:
        schedule.run_pending()
        sleep(1)


# ------- Weather (Sanjay Balasubramanian) -------

def get_location():
    """This function retrieves the location of a person using their IP address. (Done by Kapilesh Pennichetty)"""
    ext_ip = requests.get('https://api.ipify.org').text
    # (Reference: https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python)
    url = f'http://api.ipstack.com/{ext_ip}&' \
          f'output=json?' \
          f'access_key={ipstackapi_key}'  # IPStack API Documentation: https://ipstack.com/documentation
    api_output = requests.get(url)
    location_data = api_output.json()
    city = location_data["city"]
    state = location_data["region_name"]
    state_abbreviation = location_data["region_code"]
    country = location_data["country_name"]
    country_abbreviation = location_data["country_code"]
    # return only the variables required for an accurate weather search

# Start writing function definitions for weather here


# ------- Webpages (Documentation: https://flask.palletsprojects.com/en/1.1.x/ and
# https://jinja.palletsprojects.com/en/2.11.x/) -------

# ----- Home Page (Kapilesh Pennichetty) -----

@app.route("/")  # Telling Flask that the url with "/" appended at the end should lead to the home page.
def home():
    """Home page that shows trending articles."""
    return render_template('home.html', top_articles=top_headlines)
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.

# ----- Weather Page (Kapilesh Pennichetty) -----

@app.route("/weather")
def weather():
    """Page that shows weather info."""
    return render_template('weather.html')  # Rendering the HTML for the home page, passing required variables from
    # Python to HTML page using Jinja.


# ---------- Main Code ----------

# ----- Run background_fetch() in a background thread (Kapilesh Pennichetty) -----
# Reference: https://stackoverflow.com/questions/38254172/infinite-while-true-loop-in-the-background-python
fetch_articles = Thread(name='background', target=background_fetch)  # Creating thread for background task
fetch_articles.daemon = True  # Declaring that thread is a daemon (background task)
fetch_articles.start()  # Initializing the thread

# ----- Run Flask App (Kapilesh Pennichetty) -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # Telling Flask to run the app with the constraints given. (Documentation:
    # https://flask.palletsprojects.com/en/1.1.x/)
