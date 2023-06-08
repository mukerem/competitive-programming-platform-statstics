import json
import requests
from string import Template

class Leetcode:
    def __init__(self, username):
        self.username = username
        self.url = "https://leetcode.com/graphql"

    def fetch(self):
        
        body = """
        { 
            matchedUser(username: "${username}") 
            {
                username
                submitStats: submitStatsGlobal 
                {
                    acSubmissionNum 
                    {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
        """
        
        t = Template(body)
        body = t.substitute(username=self.username)
        
        response = requests.post(url=self.url, json={"query": body})

        if response.status_code == 200:
            data = json.dumps(response.json(), indent=4)
            print(data)
        else:
            print("response : ", response.content)
    

info = Leetcode("mukeremali112")
info.fetch()