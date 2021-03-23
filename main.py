# ---------- Running this Program ----------

# This program is meant to be run on a production WSGI server that supports multithreading. It will not run on
# localhost.

# ---------- Import Statements ----------
from threading import Thread
from time import sleep

import requests
import schedule
from flask import Flask, render_template, request, redirect, current_app, url_for

# ---------- API and Program Prerequisites ----------

newsapi_key = 'YOUR_NEWSAPI_KEY_HERE'  # Defining API Key for use with News API

weatherapi_key = 'YOUR_WEATHERAPI_KEY_HERE'  # Defining API Key for use with Weather API

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

# ----- List and Format Trusted News Sources -----

trusted_news_sources_list = [
    "bbc-news", "abc-news", "abc-news-au", "al-jazeera-english", "ars-technica", "associated-press",
    "australian-financial-review", "axios", "bbc-sport", "bleacher-report", "bloomberg", "business-insider", "cbc-news",
    "cbs-news", "cnn", "engadget", "espn", "financial-post", "football-italia", "fortune", "four-four-two",
    "fox-sports", "google-news", "google-news-au", "google-news-ca", "google-news-in", "google-news-uk", "independent",
    "mashable", "medical-news-today", "msnbc", "mtv-news", "mtv-news-uk", "national-geographic", "national-review",
    "nbc-news", "new-scientist", "news-com-au", "newsweek", "new-york-magazine", "nfl-news", "nhl-news", "politico",
    "polygon", "recode", "reuters", "rte", "techcrunch", "techradar", "the-globe-and-mail", "the-hill", "the-hindu",
    "the-huffington-post", "the-irish-times", "the-jerusalem-post", "the-next-web", "the-times-of-india", "the-verge",
    "the-wall-street-journal", "the-washington-post", "the-washington-times", "time", "usa-today", "vice-news", "wired"
]

trusted_news_sources = ",".join(trusted_news_sources_list)  # Formatting list for use with API


# ----- Fetching and Filtering Article Data -----

def get_top_headlines_stats():
    """Fetches Article Data and Metadata from the API"""
    url = f'https://newsapi.org/v2/top-headlines?' \
          f'sources={trusted_news_sources}&' \
          f'apiKey={newsapi_key}'
    top_headlines_stats = scrapejson(url)
    global top_headlines
    top_headlines = top_headlines_stats["articles"]
    return top_headlines


def background_fetch():
    """This function repeatedly fetches top headlines every 45 minutes."""
    get_top_headlines_stats()
    schedule.every(45).minutes.do(get_top_headlines_stats)
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
            return "Invalid Input"
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
        return "Invalid Input"


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
    ip_info = request.environ['HTTP_X_FORWARDED_FOR']
    if "," in ip_info:
        ip_addr = ip_info[:ip_info.index(",")]
    else:
        ip_addr = ip_info
    return render_template('home.html', top_articles=top_headlines, weather_icon=get_weather(ip_addr)["icon"])
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.


@app.route("/news-reliability")
def news_cred():
    """This webpage talks about the reliability and bias of the news that the app shows to the end user."""
    return render_template("news-reliability.html")


# ----- Weather Page -----


@app.route("/weather", methods=["GET", "POST"])  # Telling Flask that the URL with "/weather" appended at the end
# should lead to the weather page
def weather():
    """Page that shows weather info.
    (w/Assistance from https://www.techwithtim.net/tutorials/flask/http-methods-get-post/))"""
    if request.method == "POST":
        location = request.form["nm"]
        if get_weather(location) == "Invalid Input":
            return redirect(url_for("search_error"))
        else:
            return redirect(url_for("weather_search", place=location))
    else:
        ip_info = request.environ['HTTP_X_FORWARDED_FOR']
        if "," in ip_info:
            ip_addr = ip_info[:ip_info.index(",")]
        else:
            ip_addr = ip_info
        return render_template('weather.html',
                               temp_advice_auto=temp_commentary(get_weather(ip_addr)["temp_f"]),
                               precip_advice_auto=precip_advice(get_weather(ip_addr)["precip_in"]),
                               auto_weather=get_weather(ip_addr))
    # Rendering the HTML for the weather page, passing required variables from
    # Python to HTML page using Jinja.


@app.route("/<place>", methods=["GET", "POST"])  # Telling Flask that this is a dynamic URL, and that NewsMaster will
# find the weather for any place appended to the end of the URL.
def weather_search(place):
    """Weather Search Results Page
    (w/Assistance from https://www.techwithtim.net/tutorials/flask/http-methods-get-post/))"""
    if request.method == "POST":
        location = request.form["nm"]
        if get_weather(location) == "Invalid Input":
            return redirect(url_for("search_error"))
        else:
            return redirect(url_for("weather_search", place=location))
    else:
        return render_template("weather_search.html",
                               temp_advice_search=temp_commentary(get_weather(place)["temp_f"]),
                               search_weather=get_weather(place),
                               precip_advice_search=precip_advice(get_weather(place)["precip_in"]))  # Rendering the
        # HTML for the weather_search page, passing required variables from Python to HTML page using Jinja.


@app.route("/search_error", methods=["GET", "POST"])  # Telling Flask that the URL with /search_error appended at the
# end should lead to the search error page.
def search_error():
    """Search Error Page for when the user gives a wrong input to the search bar
    (w/Assistance from https://www.techwithtim.net/tutorials/flask/http-methods-get-post/)"""
    if request.method == "POST":
        location = request.form["nm"]
        if get_weather(location) == "Invalid Input":
            return redirect(url_for("search_error"))
        else:
            return redirect(url_for("weather_search", place=location))
    else:
        return render_template("search_error.html")  # Rendering HTML for search_error page.


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
