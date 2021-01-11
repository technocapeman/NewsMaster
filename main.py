# --- Testing done by Kapilesh Pennichetty ---
from newsapi import NewsApiClient
from flask import Flask, render_template
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY_HERE')
stats = newsapi.get_everything(q='Bitcoin')
all_articles = stats["articles"]
article=0
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('main.html', allarticles=all_articles, article=article)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)