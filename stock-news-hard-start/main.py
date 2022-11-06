import requests
from datetime import datetime, timedelta
from twilio.rest import Client


account_sid = "AC8cc0f7e59903545250d78e940fb2de58"
account_token = "aa1c3673ad176a3f4bd1e64ea0ad8050"

send_news = False

today = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
day_before_yesterday = (datetime.now() - timedelta(3)).strftime('%Y-%m-%d')

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_STOCK_TESLA = 'PR3SQR9P845HAWQG'
API_KEY_NEWS = "62ffab43c3a34c74a56cd5961f61b4ba"
parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': API_KEY_STOCK_TESLA

}

parameters_news_articles = {
    'q': 'TeslInc',
    'apiKey': API_KEY_NEWS
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
tsla_stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in tsla_stock_data.items()]
yesterday_data = data_list[0]
closing_price_yesterday = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
closing_price_the_day_before = day_before_yesterday_data["4. close"]

positive_diff_between_prices = abs(float(closing_price_yesterday) - float(closing_price_the_day_before))

if positive_diff_between_prices >= 5:
    send_news = True
    if closing_price_yesterday < closing_price_the_day_before:
        message_stock = f"TESLA: 🔻{int(positive_diff_between_prices)}%"
    else:
        message_stock = f"TESLA: 🔺{int(positive_diff_between_prices)}%"

response_news = requests.get('https://newsapi.org/v2/everything?q=TeslaInc&apiKey=62ffab43c3a34c74a56cd5961f61b4ba&to=2022-11-04', params=parameters_news_articles)
response_news.raise_for_status()
tesla_news = response_news.json()
"""
    for news_content in tesla_news['articles'][:3]:
    print(f"Headline: {news_content['title']}")
    print(f"Brief: {news_content['description']}" + "\n")
"""

if send_news:
    client = Client(account_sid, account_token)
    for news_content in tesla_news['articles'][:3]:
        message = client.messages \
                    .create(
                         body=f"{message_stock}\nHeadline: {news_content['title']}\nBrief: {news_content['description']}\n\n",
                         from_='+19804009361',
                         to='+12025107305'
                     )


#twilio_code:jb1_D-jpR1_knI2a0uFDOu-IomSIsMjTPfGvMBMA