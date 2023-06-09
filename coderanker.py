import json
import logging
from typing import Optional
import requests
from bs4 import BeautifulSoup
from string import Template

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Base:
    url: str
    username: str
    session: requests.Session = requests.Session()

    def __init__(self, username: Optional[str] = None, url: Optional[str] = None):
        self.url = url or self.url
        self.username = username

    def set_username(self, username: Optional[str] = None):
        print(username, self.username)
        username = username if username else self.username
        if not username:
            raise ValueError("Username not provided")
        return username


class Leetcode(Base):
    """
    Leetcode class to fetch user's stats from leetcode graphql endpoint

    Attributes:
        url (str): url to leetcode graphql endpoint (default: https://leetcode.com/graphql)
        username (str): username of the user whose stats are to be fetched (default: None)

    Usage:
        from coderanker import *
        leetcode = Leetcode("username")
        data = leetcode.user_info()
        print(data)

        # or 
        leetcode = Leetcode()
        data = leetcode.user_info("username") # give username as argument
    """
    url: str = "https://leetcode.com/graphql"

    def fetch(self, username: Optional[str] = None):
        """
        Fetches the user's stats from leetcode

        Args:
            username (str): username of the user whose stats are to be fetched (default: None)

        Returns:
            None if the request fails, else the json response
            data (dict): json response from leetcode graphql endpoint
                {
                    "data": {
                        "matchedUser": {
                        "username": "username",
                        "submitStats": {
                            "acSubmissionNum": [
                            { "difficulty": "All", "count": 120, "submissions": 142 },
                            { "difficulty": "Easy", "count": 100, "submissions": 100 },
                            { "difficulty": "Medium", "count": 10, "submissions": 22 },
                            { "difficulty": "Hard", "count": 10, "submissions": 20 }
                            ]
                        }
                        }
                    }
                }


        Raises:
            ValueError: if username is not provided
            Exception: if any other error occurs
        """
        try:
            username = self.set_username(username)
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
            body = t.substitute(username=username)

            response = self.session.post(url=self.url, json={"query": body})
            data = None
            if response.status_code == 200:
                data = response.json()
                logger.debug(f'Leetcode response 200: {data}')
            else:
                logger.error(f'Leetcode response {response.status_code}')

            return data
        except ValueError as e:
            logger.error(f'Leetcode fetch error: {e}')
            raise ValueError("Username not provided")

        except Exception as e:
            logger.error(f'Leetcode fetch error: {e}')
            raise Exception("Error occured while fetching data from leetcode")


class Codeforces(Base):
    """
    Codeforces class to fetch user's stats from codeforces api

    Attributes:
        url (str): url to codeforces api (default: https://codeforces.com/api)
        username (str): username of the user whose stats are to be fetched (default: None)

    Usage:
        from coderanker import *
        codeforces = Codeforces("username")
        data = codeforces.user_rating_change()
        info = codeforces.user_info()

        # or
        codeforces = Codeforces()
        data = codeforces.user_rating_change("username") # give username as argument
        info = codeforces.user_info("username") # give username as argument
    """
    url: str = "https://codeforces.com/api"

    def user_rating_change(self, username: Optional[str] = None):
        """
        Fetches the user's rating changes from codeforces api

        Args:
            username (str): username of the user whose stats are to be fetched (default: None)

        Returns:
            None if the request fails, else the json response
            data (dict): json response from codeforces api
                {
                    "status": "OK",
                    "result": [
                        {
                            "contestId": 456,
                            "contestName": "ContestX, Codefest 17",
                            "handle": "username",
                            "rank": 1000,
                            "ratingUpdateTimeSeconds": 1506272700,
                            "oldRating": 0,
                            "newRating": 1391
                        },
                        ...
                    ]
                }

        Raises:
            ValueError: if username is not provided
            Exception: if any other error occurs
        """

        # url = f"https://codeforces.com/api/user.rating?handl={username}"
        try:
            username = self.set_username(username)
            url = f"{self.url}/user.rating?handle={username}"

            response = self.session.get(url=url)
            data = None
            if response.status_code == 200:
                data = response.json()
                logger.debug(f'Codeforces response 200: {data}')
            else:
                logger.error(f'Codeforces response {response.status_code}')

            return data
        except ValueError as e:
            logger.error(f'username not provided: {e}')
            raise ValueError("Username not provided")

        except Exception as e:
            logger.error(f'Codeforces fetch error: {e}')
            raise Exception(
                "Error occurred while fetching data from codeforces")

    def user_info(self, username: Optional[str] = None):
        """
        Fetches the user's info from codeforces api

        Args:
            username (str): username of the user whose stats are to be fetched (default: None)

        Returns:
            None if the request fails, else the json response
            data (dict): json response from codeforces api
                {
                    "status": "OK",
                    "result": [
                        {
                        "lastName": "Ali",
                        "country": "Ethiopia",
                        "lastOnlineTimeSeconds": 1686205068,
                        "city": "Addis Ababa",
                        "rating": 1400,
                        "friendOfCount": 17,
                        "titlePhoto": "https://userpic.codeforces.org/522395/title/8d7e4s7r5f30639.jpg",
                        "handle": "mukeremali",
                        "avatar": "https://userpic.codeforces.org/522395/avatar/c8d9r4f5ce0be915ed.jpg",
                        "firstName": "Mukerem",
                        "contribution": 0,
                        "organization": "University",
                        "rank": "specialist",
                        "maxRating": 1476,
                        "registrationTimeSeconds": 1485501729,
                        "maxRank": "specialist"
                        }
                    ]
                }

        Raises:
            ValueError: if username is not provided
            Exception: if any other error occurs
        """
        try:
            username = self.set_username(username)
            url = f"{self.url}/user.info?handles={username}"
            response = requests.get(url=url)

            data = None
            if response.status_code == 200:
                data = response.json()
                logger.debug(f'Codeforces response 200: {data}')
            else:
                logger.error(f'Codeforces response {response.status_code}')

            return data
        except ValueError as e:
            logger.error(f'username not provided: {e}')
            raise ValueError("username not provided")
        except Exception as e:
            logger.error(f'Codeforces fetch error: {e}')
            raise Exception(
                "Error occurred while fetching data from codeforces")


class Kattis(Base):
    """
    Kattis class to fetch user's stats from kattis api

    Attributes:
        url (str): url to kattis api (default: https://open.kattis.com)
        username (str): username of the user whose stats are to be fetched (default: None)

    Usage:
        from coderanker import *
        kattis = Kattis("username")
        data = kattis.user_info()
        print(data)

        # or 
        kattis = Kattis()
        data = kattis.user_info("username") # give username as argument

    """
    url: str = "https://open.kattis.com"

    def user_info(self, username: Optional[str] = None):
        """
        Fetches the user's info from kattis api

        Args:
            username (str): username of the user whose stats are to be fetched (default: None)

        Returns:
            None if the request fails, else the json response
            data (dict): json response from kattis api
                        {
                            'Rank': '152', 'Score': '1548.6', 'username': 'username'
                        }

        Raises:
            ValueError: if username is not provided
            Exception: if any other error occurs
        """
        try:
            username = self.set_username(username)
            url = f"{self.url}/users/{username}"
            data = {"script": "true"}
            page_content = requests.get(url=url, data=data)

            if page_content.status_code != 200:
                logger.error(
                    f'Kattis response {page_content.status_code}: {page_content.content}')
                return None

            soup = BeautifulSoup(page_content.text, "html.parser")

            infos = soup.find_all('div', attrs={'class': 'divider_list-item'})
            data = {}
            for info in infos:
                spans = info.find_all('span')
                if spans:
                    key = spans[0].get_text()
                    value = spans[1].get_text()
                    data[key] = value
            if data:
                data['username'] = username
            return data if data else None
        except ValueError as e:
            logger.error(f'username not provided: {e}')
            raise ValueError("username not provided")

        except Exception as e:
            logger.error(f'Kattis fetch error: {e}')
            raise Exception("Error occurred while fetching data from kattis")
