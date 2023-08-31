import requests
from twilio.rest import Client

MY_SID = "ACca562651d2b6db0e65526d25e43cbc04"
MY_AUTH_TOKEN = "79f525e1c355cd12902bc856cdd75ac2"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api = "FNOWZ4NUDQ6FW224"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api

}


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api = "4ba1eeefec8c4154a79f871fa57d0be6"
news_params = {
    "q": COMPANY_NAME,
    "apiKey": news_api,
    "country": "sk",
    "category": "business",
    
}

try:
    stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
    # stock_response.status_code
    data = stock_response.json()["Time Series (Daily)"]
    stock_data = [value for (key, value) in data.items()]
    stock_yesterday = float(stock_data[0]["4. close"])
    stock_before = float(stock_data[1]["4. close"])

    stock_diff = abs(stock_before - stock_yesterday)

    stock_diff_per = stock_diff / stock_before * 100

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()
    new_articles = news_data["articles"][:3]
    if stock_yesterday > stock_before:
      msgs = [f"{STOCK_NAME}🔺{stock_diff_per} \nHeadlines : {article['title']}. \nBrief: {article['description']}" for article in new_articles]
    else:
       msgs = [f"{STOCK_NAME}🔻{stock_diff_per} \nHeadlines : {article['title']}. \nBrief: {article['description']}" for article in new_articles]
      

    if stock_diff_per>=3:
        client = Client(MY_SID, MY_AUTH_TOKEN)
        for msg in msgs:
            message = client.messages.create(
                body=msg,
                from_='+18643652793',
                to='+821082701817'
            )
        print("mesg success")
        
except requests.exceptions.RequestException as e:
    print("An error occurred during API request:", e)

except Exception as e:
    print("An error occurred:", e)

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

