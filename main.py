# ---------- Import Statements ----------
from threading import Thread
from time import sleep

import requests
import schedule
from flask import Flask, render_template, request, redirect, url_for

# ---------- API and Program Prerequisites ----------

newsapi_key = 'YOUR_NEWSAPI_KEY_HERE'  # Defining API Key for use with News API

weatherapi_key = 'YOUR_WEATHERAPI_KEY_HERE'  # Defining API Key for use with Weather API

app = Flask(__name__)  # Defining Flask App (Source: https://flask.palletsprojects.com/en/1.1.x/)

# -------- Credits ----------
"""
- News headlines, source names, publication dates, descriptions, images, and links to articles are from the News API; please visit newsapi.org for more details
- Weather data from Weather API, please visit weatherapi.com
"""

# ---------- Functions and Data ----------

# ------- Trending News (Kapilesh Pennichetty) -------

# ----- List and Format Trusted News Sources -----

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
    """This function repeatedly calls fetch_top_headlines() every 45 minutes
     (Documentation: https://schedule.readthedocs.io/en/stable/index.html)."""
    fetch_top_headlines()
    schedule.every(45).minutes.do(fetch_top_headlines)
    while True:
        schedule.run_pending()
        sleep(1)


# ------- Weather (Kapilesh Pennichetty and Sanjay Balasubramanian) -------


def scrapejson(jsonurl):
    """This function scrapes a URL to get the JSON file at the URL. (Made by Kapilesh Pennichetty)"""
    api_output = requests.get(jsonurl)
    data = api_output.json()
    return data


def get_weather(location):  # location can be IP address, city, or ZIP
    """This function takes the location and outputs the current weather. (Done by
    Kapilesh Pennichetty)"""
    url = f"https://api.weatherapi.com/v1/current.json?" \
          f"key={weatherapi_key}&" \
          f"q={location}"
    stats = {"temp_f": 0, "wind_mph": 0, "wind_dir": "", "humidity": 0, "precip_in": 0.0, "feelslike_f": 0,
             "text": "", "icon": "", "location": ""}
    error_message = "Error: Make sure your parameter is correct."
    try:
        weather_data = scrapejson(url)['current']
        if "error" in weather_data:
            return error_message
        else:
            for stat in stats:
                if stat == "text":
                    stats[stat] = weather_data['condition'][stat]
                elif stat == "icon":
                    stats[stat] = "https:" + weather_data['condition'][stat]
                elif stat == "location":
                    stats[stat] = scrapejson(url)[stat]["name"]
                else:
                    stats[stat] = weather_data[stat]
            return stats
    except:
        return error_message


def temp_commentary(current_temp):
    """Gives temperature advice to the end user. (Done by Sanjay Balasubramanian)"""
    temperature = int(current_temp)
    temperature_level = {
        0: "It's scorching hot. Stay inside and be cool!",
        1: "It's hot and sunny. Don't forget that sunscreen!",
        2: "It's nice and warm today. Time to flex those flip-flops!",
        3: "It's nice and cool today. Go play outside in this great weather!",
        4: "It's gonna be cold today. Make sure you keep yourself warm!",
        5: "Brrrrrrr!!! Remember to wear your protective wear so you don't freeze!",
        6: "It's Freezing Cold. Staying inside and a cup of Hot chocolate would be nice!"
    }

    if temperature >= 95:
        return temperature_level[0]
    elif 80 <= temperature <= 94:
        return temperature_level[1]
    elif 69 <= temperature <= 79:
        return temperature_level[2]
    elif 59 <= temperature <= 68:
        return temperature_level[3]
    elif 40 <= temperature <= 57:
        return temperature_level[4]
    elif 25 <= temperature <= 39:
        return temperature_level[5]
    elif temperature <= 24:
        return temperature_level[6]


def precip_advice(precip_in):
    """Gives precipitation advice to the end user (Done by Sanjay Balasubramanian and Kapilesh Pennichetty)"""
    precipitation_level = {0: "There is low to no chance of rain. No need for an umbrella.",
                           1: "There is a moderate chance of rain. Grab an umbrella on your way out just in case. ☔",
                           2: "It is definitely going to rain today! GRAB YOUR UMBRELLA AND YOUR RAINCOAT. ☔ 🧥"}

    if precip_in <= .1:
        return precipitation_level[0]
    elif .1 < precip_in < .3:
        return precipitation_level[1]
    elif precip_in >= 0.3:
        return precipitation_level[2]


# ------- Webpages (Documentation: https://flask.palletsprojects.com/en/1.1.x/ and
# https://jinja.palletsprojects.com/en/2.11.x/) -------

# ----- Home Page (Kapilesh Pennichetty) -----

@app.route("/",
           methods=['GET'])  # Telling Flask that the url with "/" appended at the end should lead to the home page.
def home():
    """Home page that shows trending articles. (Done by Kapilesh Pennichetty)"""
    ip_info = request.environ['HTTP_X_FORWARDED_FOR']
    if "," in ip_info:
        ip_addr = ip_info[:ip_info.index(",")]
    else:
        ip_addr = ip_info
    return render_template('home.html', top_articles=top_headlines, weather_icon=get_weather(ip_addr)["icon"])
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.


# ----- Weather Page -----


@app.route("/weather", methods=["GET", "POST"])
def weather():
    """Page that shows weather info. (Done by Kapilesh Pennichetty and Sanjay Balasubramanian
    (w/Assistance from https://www.techwithtim.net/tutorials/flask/http-methods-get-post/)"""
    if request.method == "POST":
        location = request.form["nm"]
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
        # Rendering the HTML for the home page, passing required variables from
        # Python to HTML page using Jinja.


@app.route("/<place>")
def weather_search(place):
    """Weather Search Results Page (Done by Kapilesh Pennichetty
    (w/Assistance from https://www.techwithtim.net/tutorials/flask/http-methods-get-post/))"""
    if (place is False) or (place == ""):
        return "Cannot find location. Please make sure that your search input is correct."
    else:
        return render_template("weather_search.html", temp_advice_search=temp_commentary(get_weather(place)["temp_f"]),
                               search_weather=get_weather(place),
                               precip_advice_search=precip_advice(get_weather(place)["precip_in"]))


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
