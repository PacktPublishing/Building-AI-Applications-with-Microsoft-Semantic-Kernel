import os
from dotenv import load_dotenv
import requests
import json

class BingSearch:
    def __init__(self):
        load_dotenv("linkedin.env")
        # save the access token to the class
        self.access_token = os.getenv("BING_KEY")

    def parse(self, json_string):
        # Load the JSON data into a Python dictionary
        data = json.loads(json_string)
        
        # Extract the "value" list which contains the news articles
        news_articles = data.get("value", [])
        
        # Extract the name and description for each article
        articles_info = [{"name": article.get("name"), "description": article.get("description")} for article in news_articles]
        
        return articles_info
        
    def TopTechNewsToday(self):
        url = "https://api.bing.microsoft.com/v7.0/news/search"
        headers = {
            "Ocp-Apim-Subscription-Key": f"{self.access_token}",
        }
        query = "most important technology releases today"
        params = {
            "q": query,
            "category": "Technology",
            "count": "5",
            "mkt": "en-US",
            "freshness": "Day"
        }
        response = requests.get(url, headers=headers, params=params)
        # check if the response is successful
        if response.status_code == 200:
            return self.parse(response.text)
        else:
            action = f"Error: {response.status_code}."
            action += "\nDetails: " + response.text
            return action