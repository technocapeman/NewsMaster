# ---------- Import Statements ----------
from threading import Thread
from time import sleep

import requests
import schedule
from flask import Flask, render_template, request

# ---------- API and Program Prerequisites ----------

newsapi_key = 'YOUR_NEWSAPI_KEY_HERE'  # Defining API Key for use with News API

weatherapi_key = 'YOUR_WEATHERAPI_KEY_HERE'  # Defining API Key for use with Weather API

ipstackapi_key = 'c4b64d4441b6342c27001dc87593d4f0'  # Defining API Key for use with IPStack API

app = Flask(__name__)  # Defining Flask App (Source: https://flask.palletsprojects.com/en/1.1.x/)

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

major_cities = ["Austin", "New York City", "London", "Sydney", "Tokyo"]


def scrapejson(jsonurl):
    """This function scrapes a URL to get the JSON file at the URL. (Made by Kapilesh Pennichetty)"""
    api_output = requests.get(jsonurl)
    data = api_output.json()
    return data


def get_location(ip_address):
    """This function retrieves the location of a person using their IP address. (Done by Kapilesh Pennichetty)"""
    ext_ip = requests.get('https://api.ipify.org').text
    # (Reference: https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python)
    url = f'http://ip-api.com/json/{ip_address}'
    location_data = scrapejson(url)
    city = location_data["city"]
    return city


def get_weather(location):  # location can be IP address, city, or ZIP
    """This function takes the location and outputs the current weather. (Made by
    Kapilesh Pennichetty and Sanjay Balasubramanian)"""
    url = f"https://api.weatherapi.com/v1/current.json?" \
          f"key={weatherapi_key}&" \
          f"q={location}"
    stats = {"temp_f": 0, "wind_mph": 0, "wind_dir": "", "humidity": 0, "precip_in": 0.0, "uv": 0.0, "feelslike_f": 0}
    try:
        weather_data = scrapejson(url)['current']
        if "error" in weather_data:
            return False
        else:
            for stat in stats:
                stats[stat] = weather_data[stat]
            description = weather_data['condition']['text']
            current_temp = stats["temp_f"]
            wind_speed = stats["wind_mph"]
            wind_direction = stats["wind_dir"]
            humidity = stats["humidity"]
            uv_index = stats["uv"]
            feels_like = stats["feelslike_f"]
            precipitation = stats["precip_in"]
            location = weather_data["location"]["name"]
            return description, current_temp, wind_speed, wind_direction, humidity, uv_index, feels_like, precipitation, location
    except:
        return False


def major_cities_weather():
    """This function finds and returns the weather of the major cities. (Done by Kapilesh Pennichetty)"""
    cities_weather = []

    for city in major_cities:
        city_weather = get_weather(city)
        cities_weather.append(city_weather)

    Austin_Weather = cities_weather[0]
    NYC_Weather = cities_weather[1]
    London_Weather = cities_weather[2]
    Sydney_Weather = cities_weather[3]
    Tokyo_Weather = cities_weather[4]

    return Austin_Weather, NYC_Weather, London_Weather, Sydney_Weather, Tokyo_Weather


# ------- Webpages (Documentation: https://flask.palletsprojects.com/en/1.1.x/ and
# https://jinja.palletsprojects.com/en/2.11.x/) -------

# ----- Home Page (Kapilesh Pennichetty) -----

@app.route("/")  # Telling Flask that the url with "/" appended at the end should lead to the home page.
def home():
    """Home page that shows trending articles."""
    return render_template('home.html', top_articles=top_headlines)
    # Rendering the HTML for the home page, passing required variables from Python to the HTML page using Jinja.


# ----- Weather Page -----

def weather_commentary(current_temp):
    temperature = int(current_temp)
    temperature_level = {
        0: "It's scorching hot. Stay inside and be cool!",
        1: "It's hot and sunny. Don't forget that sunscreen!",
        2: "It's nice and warm today. Time to flex those flip-flops",
        3: "It's nice and cool today . Go play outside in this great weather",
        4: "It's gonna be cold today. Make sure you keep yourself warm!",
        5: "Brrrrrrr!!! Remember to wear your protective wear so you don't freeze.",
        6: "It's Freezing Cold. Staying inside and a cup of Hot chocolate would be nice. "
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


"""Precipitation_WARNING = data['daily']['data'][0]['precipProbability']
Precipitation_level = {
                    0:  "there is a slight chance of rain. " \
                        "You might want to grab an umbrella ☔",
                    1:  "there is a high chance of rain. " \
                        "Grab an umbrella on your way out! ☔",
                    2:  "it is raining right now!",
                    3:  "it is definitely going to rain today! " \
                        "GRAB YOUR UMBRELLA. ☔"
                }
    if Precipitation_WARNING == 0:
        Precipitation_commentary = weather_commentary(temperature)
    elif 0 < Precipitation_WARNING <= .5:
        Precipitation_commentary = Precipitation_level[0]
    elif .5 < Precipitation_WARNING < .75:
        Precipitation_commentary = Precipitation_level[1]
    elif Precipitation_WARNING == 1:
        Precipitation_commentary = Precipitation_level[2]
    else:
        Precipitation_commentary = Precipitation_level[3]
"""


@app.route("/weather", methods=["GET"])
def weather():
    """Page that shows weather info."""
    ip_info = request.environ['HTTP_X_FORWARDED_FOR']
    if "," in ip_info:
        ip_addr = ip_info[:ip_info.index(",")]
    else:
        ip_addr = ip_info

    return render_template('weather.html', auto_weather=get_weather(get_location(ip_addr)),
                           austin_weather=major_cities_weather()[0],
                           NYC_weather=major_cities_weather()[1], london_weather=major_cities_weather()[2],
                           sydney_weather=major_cities_weather()[3], tokyo_weather=major_cities_weather()[
            4])  # Rendering the HTML for the home page, passing required variables from
    # Python to HTML page using Jinja.


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip_info = request.environ['HTTP_X_FORWARDED_FOR']
    """if "," in ip_info:
        ip_addr = ip_info[:ip_info.index(",")]
    else:
        ip_addr = ip_info

    return ip_addr"""

    return ip_info


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
