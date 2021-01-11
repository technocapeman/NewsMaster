# --- Testing done by Kapilesh Pennichetty ---
from newsapi import NewsApiClient
from flask import Flask, render_template
newsapi = NewsApiClient(api_key='eadbfa9229d14334b96c95ccd2d733e1')
stats = newsapi.get_everything(q='Donald Trump')
all_articles = stats["articles"]
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('main.html', allarticles=all_articles)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)