# ---------- Running this Program ----------

# Install all requirements from requirements.txt prior to running this program. Use the following command:
# pip install -r requirements.txt

# The stable branch of this program should only be run on a production WSGI server, such as Heroku.

# ---------- Import Statements ----------
import os
from threading import Thread
from time import sleep

import requests
import schedule
from flask import Flask, render_template, request, current_app

# ---------- API and Program Prerequisites ----------

newsapi_key = os.environ.get("NEWSAPI_KEY")  # Defining API Key for use with News API

weatherapi_key = os.environ.get("WEATHERAPI_KEY")  # Defining API Key for use with Weather API

app = Flask(__name__)  # Defining Flask App (Source: https://flask.palletsprojects.com/en/1.1.x/)

# -------- Credits ----------
"""
- News headlines, source names, publication dates, descriptions, images, and links to articles are from News API;
please visit https://newsapi.org for more details
- Weather data from Weather API; please visit https://weatherapi.com for more details.
- Scheduling News Article Fetch: https://schedule.readthedocs.io/en/stable/index.html
- Search Functionality: https://www.techwithtim.net/tutorials/flask/http-methods-get-post
- Using Background Threads: 
https://stackoverflow.com/questions/38254172/infinite-while-true-loop-in-the-background-python
- Integrating Service Worker with Flask: 
https://www.reddit.com/r/PWA/comments/bmsed8/this_is_how_i_install_my_service_worker_using/
"""


# ---------- Functions and Data ----------

def scrapejson(jsonurl):
    """This function scrapes a URL to get the JSON file at the URL."""
    api_output = requests.get(jsonurl)
    data = api_output.json()
    return data


# ------- Trending News -------

article_num = 30  # Defining number of news articles to show

# ----- List and Format Trusted News Sources -----

trusted_news_sources_list = [
    "abc-news", "abc-news-au", "al-jazeera-english", "ars-technica", "associated-press", "australian-financial-review",
    "axios", "bbc-news", "bbc-sport", "bleacher-report", "bloomberg", "business-insider", "cbc-news", "engadget",
    "espn", "financial-post", "fortune", "fox-sports", "independent", "medical-news-today", "national-geographic",
    "nbc-news", "new-scientist", "news-com-au", "newsweek", "nfl-news", "nhl-news", "politico", "polygon", "recode",
    "reuters", "rte", "techcrunch", "techradar", "the-globe-and-mail", "the-hill", "the-hindu", "the-irish-times",
    "the-jerusalem-post", "the-next-web", "the-times-of-india", "the-verge", "the-wall-street-journal",
    "the-washington-post", "time", "usa-today", "vice-news", "wired"
]

trusted_news_sources = ",".join(trusted_news_sources_list)  # Formatting list for use with API


# ----- Fetching and Filtering Article Data -----

def fetch_top_headlines():
    """Fetches Article Data and Metadata from the API"""
    url = f'https://newsapi.org/v2/top-headlines?' \
          f'sources={trusted_news_sources}&' \
          f'apiKey={newsapi_key}&' \
          f'pageSize={article_num}'
    top_headlines_stats = scrapejson(url)
    global top_headlines
    top_headlines = top_headlines_stats["articles"]


def background_fetch():
    """This function repeatedly fetches top headlines every 45 minutes."""
    fetch_top_headlines()
    schedule.every(15).minutes.do(fetch_top_headlines)
    while True:
        schedule.run_pending()
        sleep(1)


# ------- Weather -------

def get_weather(location):  # location can be IP address, city, or ZIP
    """This function takes the location and outputs the current weather."""
    url = f"https://api.weatherapi.com/v1/current.json?" \
          f"key={weatherapi_key}&" \
          f"q={location}"
    stats = {"temp_f": 0, "wind_mph": 0, "wind_dir": "", "humidity": 0, "precip_in": 0.0, "feelslike_f": 0,
             "text": "", "icon": "", "name": "", "last_updated": "", "tz_id": ""}
    try:
        weather_data = scrapejson(url)
        if "error" in weather_data:
            return False
        else:
            for stat in stats:
                if stat in weather_data["current"]["condition"]:
                    stats[stat] = weather_data['current']['condition'][stat]
                elif stat in weather_data["location"]:
                    stats[stat] = weather_data['location'][stat]
                else:
                    stats[stat] = weather_data['current'][stat]
            return stats
    except:
        return False


def temp_commentary(current_temp):
    """Gives temperature advice to the end user."""
    temperature = int(current_temp)
    temperature_level = {
        0: "It's scorching hot right now. Stay inside and be cool!",
        1: "It's hot and sunny right now. Don't forget that sunscreen!",
        2: "It's nice and warm right now. Time to flex those flip-flops!",
        3: "It's nice and cool right now. Go play outside in this great weather!",
        4: "It's cold right now. Make sure you keep yourself warm!",
        5: "Brrrrrrr!!! Remember to wear your protective gear so you don't freeze!",
        6: "It's Freezing Cold. Staying inside and a cup of Hot chocolate would be nice!"
    }

    if temperature >= 95:
        return temperature_level[0]
    elif 80 <= temperature < 95:
        return temperature_level[1]
    elif 69 <= temperature < 80:
        return temperature_level[2]
    elif 59 <= temperature < 69:
        return temperature_level[3]
    elif 40 <= temperature < 59:
        return temperature_level[4]
    elif 25 <= temperature < 40:
        return temperature_level[5]
    elif temperature < 25:
        return temperature_level[6]


def precip_advice(precip_in):
    """Gives precipitation advice to the end user"""
    precipitation_level = {0: "There is low to no precipitation.",
                           1: "There is a moderate amount of precipitation. Take necessary precautions.",
                           2: "There is a high amount of precipitation! Be careful outside!"}

    if precip_in <= .1:
        return precipitation_level[0]
    elif .1 < precip_in < .3:
        return precipitation_level[1]
    elif precip_in >= 0.3:
        return precipitation_level[2]


# ------- Webpages -------

# ----- Home Page -----

@app.route("/", methods=['GET'])  # Telling Flask that the URL with "/" appended at the end should lead to the home
# page.
def home():
    """Home page that shows trending articles."""
    # Get the IP address of the user and fetch weather data for the ip address.
    # NOTE: The IP address code for the production (stable) branch is not the same as the code for the dev branch
    # For testing purposes, the dev branch uses code for server IP rather than client IP.
    # This code will automatically be modified to client IP when merging from dev to stable.
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    weather = get_weather(ip_addr)
    return render_template('home.html', top_articles=top_headlines, weather_icon=weather["icon"],
                           temp=weather["temp_f"])
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.


@app.route("/news-reliability")
def news_reliability():
    """This webpage talks about the reliability and bias of the news that the app shows to the end user."""
    title = "News Reliability and Bias | NewsMaster"
    return render_template("news-reliability.html", title=title)


# ----- Weather Page -----

@app.route("/weather", methods=["GET", "POST"])  # Telling Flask that the URL with "/weather" appended at the end
# should lead to the weather page
def weather():
    """Page that shows weather info.
    (w/Assistance from https://www.techwithtim.net/tutorials/flask/http-methods-get-post/))"""
    if request.method == "POST":
        location = request.form["nm"]
        weather = get_weather(location)
        if not weather:
            title = "Search Error | NewsMaster"
            return render_template('weather.html', isValid=False, title=title)
        else:
            title = f"{weather['name']} Weather | NewsMaster"
            return render_template('weather.html',
                                   temp_advice=temp_commentary(weather["temp_f"]),
                                   precip_advice=precip_advice(weather["precip_in"]),
                                   weather=weather, isValid=True, title=title)
    else:
        # Get the IP address of the user and fetch weather data for the ip address.
        # NOTE: The IP address code for the production (stable) branch is not the same as the code for the dev branch
        # For testing purposes, the dev branch uses code for server IP rather than client IP.
        # This code will automatically be modified to client IP when merging from dev to stable.
        ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        weather = get_weather(ip_addr)
        title = f"{weather['name']} Weather | NewsMaster"
        return render_template('weather.html',
                               temp_advice=temp_commentary(weather["temp_f"]),
                               precip_advice=precip_advice(weather["precip_in"]),
                               weather=weather, isValid=True, title=title)
    # Rendering the HTML for the weather page, passing required variables from
    # Python to HTML page using Jinja.


# ----- Service Worker -----
@app.route('/service-worker.js', methods=['GET'])
def sw():
    """Integrates Service Worker with Flask (Credits:
    https://www.reddit.com/r/PWA/comments/bmsed8/this_is_how_i_install_my_service_worker_using/)"""
    return current_app.send_static_file('service-worker.js')


# ---------- Main Code ----------

# ----- Run background_fetch() in a background thread -----
# Reference: https://stackoverflow.com/questions/38254172/infinite-while-true-loop-in-the-background-python
fetch_articles = Thread(name='background', target=background_fetch)  # Creating thread for background task
fetch_articles.daemon = True  # Declaring that thread is a daemon (background task)
fetch_articles.start()  # Initializing the thread

# ----- Run Flask App -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # Telling Flask to run the app with the constraints given. (Documentation:
    # https://flask.palletsprojects.com/en/1.1.x/)
