"""
    This file takes in the broken json data and strips it away to "useable" data    
"""
import re
import requests
from bs4 import BeautifulSoup as bs
from link_data import LINK

class A_data:
    """
        Class used to store data to be used in freetweet
    """
    def __init__(self):
        self.username: str = ""
        self.all_link_ids: list = []
        self.users_ids: list = []
        self.users_rt_ids: list = []
    
    def set_username(self, name: str) -> None:
        self.username = name
        
    def get_username(self) -> str:
        return self.username
    
    def get_all_links(self) -> str:
        return self.all_link_ids
    
    def get_user_tweets(self) -> str:
        return self.users_ids
    
    def get_user_retweets(self) -> str:
        return self.users_rt_ids
    
    def add_id(self, id: str):
        if id not in self.all_link_ids:
            self.all_link_ids.append(id)
            if re.search('^https://twitter.com/' + self.username + "/status/\d*$", id):
                self._add_user_id(id)
            else:
                self._add_rt_id(id)
                
    def _add_rt_id(self, id: str) -> None:
        self.users_rt_ids.append(id)
    
    def _add_user_id(self, id: str) -> None:
        self.users_ids.append(id)
    
    def print_all_tweets(self) -> None:
        print("User's tweets:")
        for user_tweet in self.users_ids:
            print(user_tweet)
        print("User's retweets:")
        for rt_tweet in self.users_rt_ids:
            print(rt_tweet)
            

def pull_and_process_data(username: str) -> A_data:
    """
        Function takes in a username and returns the missing tweets. Data is converted from a 
        Response to Str, then read into BeautifulSoup to search for links within it
        
    Args:
        :param username: String - The username to be looked up
        :param new_data: A-data - Stores data over current user
        :param web_page: Response - Gets the extra data from Twitter that's missing from normal querries  
        :param to_text: String - 
    """
    new_data = A_data()
    if username == "":
        return new_data

    web_page = requests.get(LINK
                            .replace("USERNAME", username)
                            .replace("USER_REPLIES", "false")
                            .replace("USER_RETWEETS", "false"))
    to_text = web_page.text.replace("\\n", '').replace("\\", '')
    soup = bs(to_text, "html.parser")
    for link in soup.findAll('a'):
        if re.search('^https://twitter.com/.*/status/\d*$', link.get('href')):
            new_data.add_id(link.get('href'))
    return new_data

def main() -> None:
    tweet_data = pull_and_process_data("diivesart")
    tweet_data.print_all_tweets()

if __name__ == "__main__":
    main()