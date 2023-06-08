import json
import requests
from bs4 import BeautifulSoup
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


class Kattis:
    def  __init__(self, username):
        self.username = username
    
    def user_info(self):
        url = f"https://open.kattis.com/users/{self.username}"
        data = {"script": "true"}
        page_content = requests.get(url=url, data=data)
        soup = BeautifulSoup(page_content.text, "html.parser")
 
        infos = soup.find_all('div', attrs={'class':'divider_list-item'})
        data = {}
        for info in infos:
            spans = info.find_all('span')
            if spans:
                key = spans[0].get_text()
                value = spans[1].get_text()
                data[key] = value

        print(data)


info = Leetcode("mukeremali112")
info.fetch()

info = Codeforces("mukeremali")
info.user_info()

info = Kattis("mukerem")
info.user_info()