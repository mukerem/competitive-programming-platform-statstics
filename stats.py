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
    

class Codeforces:
    def __init__(self, username):
        self.username = username

    def user_rating_change(self):
        url = f"https://codeforces.com/api/user.rating?handle={self.username}"

        response = requests.get(url=url)

        if response.status_code == 200:
            data = json.dumps(response.json(), indent=4)
            print(data)
        else:
            print("response : ", response.content)
    
    def user_info(self):
        url = f"https://codeforces.com/api/user.info?handles={self.username}"
        response = requests.get(url=url)

        if response.status_code == 200:
            data = json.dumps(response.json(), indent=4)
            print(data)
        else:
            print("response : ", response.content)

leetcode = Leetcode("mukeremali112")
leetcode.fetch()

codeforces = Codeforces("mukeremali")
codeforces.user_info()