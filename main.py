# ---------- Import Statements (Kapilesh Pennichetty) ----------
import threading
import time
from datetime import date, timedelta

import schedule
from flask import Flask, render_template
from newsapi import NewsApiClient


# ---------- API and Program Prerequisites (Kapilesh Pennichetty) ----------

# -- News API Prerequisites (Kapilesh Pennichetty) --
newsapi = NewsApiClient(api_key='20ca56b0d34349b59d3461d638a18f16')  # Registering API Key for Use and Abstracting
# Key Away (Source: https://newsapi.org/docs)

# -- Flask Framework Prerequisites (Kapilesh Pennichetty) --
app = Flask(__name__)  # Source: https://flask.palletsprojects.com/en/1.1.x/


# ---------- Defining Classes, Functions, and Variables ----------

# ----- Format News Sources (Kapilesh Pennichetty) -----
trusted_news_sources = [
    "bbc-news", "abc-news", "abc-news-au", "al-jazeera-english",
    "ars-technica", "associated-press", "australian-financial-review", "axios",
    "bbc-sport", "bleacher-report", "bloomberg", "breitbart-news",
    "business-insider", "cbc-news", "cbs-news", "cnn", "crypto-coins-news",
    "engadget", "espn", "financial-post",
    "football-italia", "fortune", "four-four-two", "fox-news", "fox-sports",
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

# ----- Fetch Articles -----

# -- Defining Article Date Range (Kapilesh Pennichetty) --
# (Source: https://stackoverflow.com/questions/703907/how-would-i-compute-exactly-30-days-into-the-past-with-python-down-to-the-minut)

from_date = date.today() - timedelta(30)  # Defining a variable to tell the API to return articles
# as far as 30 days back using datetime module.

to_date = date.today()  # Defining a variable to tell the API to return articles until today using datetime module.


# -- Fetching and Filtering Article Data (Kapilesh Pennichetty) --
def get_top_headlines_stats():
    """Fetches Article Data and Metadata from the API (Source: https://newsapi.org/docs)"""
    top_headlines_stats = newsapi.get_top_headlines(  # Requesting data from the News API about the top headlines
        sources=format_trusted_news_sources(),
        language='en')
    return top_headlines_stats


def get_top_articles():
    """Filters out article data from API metadata"""
    all_top_articles = get_top_headlines_stats()[
        "articles"]  # Separating articles from the search query data
    return all_top_articles

"""
To be used when developing search bar, filters, and sorting:
all_articles_stats = newsapi.get_everything(sources=format_trusted_news_sources(),  # Requesting data from the News 
# API 
# about all articles
                                      from_param=from_date,
                                      to=to_date,
                                      language='en',
                                      sources=format_trusted_news_sources(),
                                      language='en',
                                      sort_by='relevancy')

all_articles = all_articles_stats["articles"]  # Separating articles from the search query data

Reminder: Be sure to pass the variable all_articles to the HTML page.
"""

# -- Using Scheduler to Fetch Articles (Kapilesh Pennichetty) --
class AutoSchedule(object):
    """Class that Allows Scheduler to Run in a Background Thread"""

    def __init__(self, interval=1):
        """Declares and Initiates a Background Thread for fetching news articles (Source:
    https://dev.to/hasansajedi/running-a-method-as-a-background-process-in-python-21li)"""
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())  # Declaring Thread
        thread.daemon = True  # Assigning thread property of background task (daemon)
        thread.start()

    def run(self):
        """Runs a While loop to keep checking if there are any pending scheduled tasks. (Source:
        https://schedule.readthedocs.io/en/stable/) """
        while True:
            schedule.run_pending()
            time.sleep(self.interval)


# ----- Webpages (Source: https://flask.palletsprojects.com/en/1.1.x/ and
# https://jinja.palletsprojects.com/en/2.11.x/) -----

# -- Home Page (Kapilesh Pennichetty) --
@app.route("/")  # Telling Flask that the url with "/" appended at the end should lead to the home page.
def home():
    """Home page that shows trending articles."""
    return render_template('home.html', all_top_articles=get_top_articles())  # Rendering the HTML for the home page,
    # passing required variables from Python to the HTML page using Jinja.


# ---------- Main Code ----------

# ----- Initializing Flask App (Kapilesh Pennichetty) -----
if __name__ == "__main__":
    app.run(
        host='0.0.0.0', port=5000, debug=True, threaded=True
    )  # Telling Flask to run the app with the constraints given. (Source: https://flask.palletsprojects.com/en/1.1.x/)

# ----- Other Tasks -----

# -- Scheduler Tasks (Kapilesh Pennichetty) --

# Adding tasks to Scheduler (Source: https://schedule.readthedocs.io/en/stable/)
schedule.every(15).minutes.do(get_top_headlines_stats)  # Requests articles and stats from the API per set time
schedule.every(15).minutes.do(get_top_articles)  # Separates articles from search query data per set time

# Run methods (functions) in the AutoSchedule Class
AutoSchedule()
