import os
from dotenv import load_dotenv
import json
import requests

class LinkedInPoster:
    def __init__(self):
        load_dotenv("linkedin.env")
        # save the access token to the class
        self.access_token = os.getenv("LINKEDIN_NEW_TOKEN")
        self.person_id = os.getenv("LINKEDIN_PERSON_ID")
        pass
        
    def CreateTextPost(self, content: str) -> str:
        # load text_share.json
        data = {}
        with open('text_share.json') as json_file:
            data = json.load(json_file)
            data['author'] = f"{self.person_id}"
            data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"] = f"{content}"

        # use requests to post the data to the LinkedIn API
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # check if the response is successful
        if response.status_code == 201:
            action = f"Success."
            return action
        else:
            action = f"Error: {response.status_code}."
            action += "\nDetails: " + response.text
            return action


    def CreateMediaPost(self, content: str, image_url: str) -> str:
        action = f"Created a media post with content {content} and image URL {image_url}."
        print(action)
        return action