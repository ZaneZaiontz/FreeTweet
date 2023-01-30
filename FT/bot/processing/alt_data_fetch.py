"""
    This file takes in the data from nitter and processes it 
"""
import re
import requests
from bs4 import BeautifulSoup as bs
from .link_data import LINK

class A_data:
    """
    Class used to store data to be used in freetweet

    :param username:
    :param link_id_set:
    :param got_all_requested: Bool, used to tell if all data requested was found
    """
    def __init__(self):
        """
        Constructor
        """
        self.username: str = ""
        self.link_id_set: set = set()
        self.got_all_requested = False
    
    def set_username(self, name: str) -> None:
        """
        Sets the username for the class

        :param name: Name to set username to
        """
        self.username = name

    def set_new_id(self, twt_id: str) -> None:
        """
        Checks current list and adds
        """
        self.link_id_set.add(twt_id)

    def set_got_all_req(self, status: bool) -> None:
        """
        Sets class status if all data was correctly received
        """

    def get_all_req(self) -> bool:
        """
        Returns the status of all data

        :returns: status of all data
        """
        return self.got_all_requested

    def get_username(self) -> str:
        """
        Returns the set username

        :returns: The set username
        """
        return self.username

    def get_all_ids(self) -> list:
        """
        Gets list of all IDs added to class

        :returns: List of all IDs added to class
        """
        return list(self.link_id_set)

    def print_all_tweets(self) -> None:
        """
        Prints out all IDs stored for selected user
        """
        print("User's IDs:")
        for user_tweet in self.link_id_set:
            print(user_tweet)

def pull_and_process_data(username: str, num_tweets: int) -> A_data:
    """
    Function takes in a username and returns the missing tweets. Data is converted from a 
    Response to Str, then read into BeautifulSoup to search for links within it. Currently
    only focuses on tweets with images
        
    Args:
        :param username: String - The username to be looked up
        :param new_data: A-data - Stores data over current user
        :param web_page: Response - Gets the extra data from Twitter that's normally missing
        :param to_text: String - 
    """
    new_data = A_data()
    
    if not username:
        print("No username was passed, returning...")
        return new_data

    new_link = LINK.replace("USERNAME", username) #.replace("USER_REPLIES", "false").replace("USER_RETWEETS", "false")
    new_link += "/media"
    web_page = requests.get(new_link)
    soup = bs(web_page.text, "html.parser")

    if not soup.find("div", {"class":"error-panel"}):
        for link in soup.findAll('a',{"class":"tweet-link"}):
            if len(new_data.link_id_set) >= num_tweets:
                print("Number of tweets requested found, breaking out early")
                new_data.set_got_all_req(True)
                break
            if re.search('\d{19}', link.get('href')):
                print(f"found ID {link.get('href')}")
                new_data.set_new_id(re.search('\d{19}', link.get('href')).group())
        print(f"ALT\n{new_data.get_all_ids()}")
    return new_data