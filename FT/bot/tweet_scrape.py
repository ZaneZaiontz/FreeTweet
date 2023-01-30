"""
    This file handles scriping twitter data and planning for future uses. The main purpose of this is to pull data from creators to be 
    posted to a discord channel and update the users who requested it.

    Future features:
        - Ability to follow creators
        - Ability to unfollow creators
        - Add class that keeps track of server follows
        - Auto-update for Twitter timeline
        - Ability to filter what types of tweets are posted by the bot (such as only images, only replies, etc.)
        - Upon following, ability to post the last X number of posts (most likely will have a 5 tweet limit to start)
        - Set auto-update frequency (For now with a min time of every 5 minutes)
        - Ability to check tweet record and ONLY post new posts that the bot has yet to post
        - Flags set per creator, such as if the work should be posted with a spoiler tag
        - Ability to scan tweet and alert server/users depending on what the tweet says
        - If you're looking for the word combinations, the bot will @ the user(s) who want to be notified

    TODO:
        - Add threading
        - Change link depending on gallery-gif or gallery-video
        - Add '/' command
"""
import os
import logging
import twint
import pandas
from main import FreeBot
import bot.processing.alt_data_fetch as extra_data
from .processing import link_conversion

def get_tweet(free_bot: FreeBot) -> list[str]:
    """
        Function uses twint to pull tweets from requested user, if user needs additional data, 
        pulls from private nitter instance if available

        :prarm username: Name of the user being looked up
        :prarm num_tweets: Number of tweets pulls *Keep around MAX 20 tweets*
        :prarm fetch_missing: Bool used as a flag if the user will wants data scrapped from nitter

        :returns: A tuple containing the list of tweets and a status code
    """
    fin_output = []
    if free_bot.get_additional():
        fin_output = get_missing_tweets(free_bot)
    else:
        test_driver = twint.Config()
        test_driver.Hide_output = True
        test_driver.Username = free_bot.get_username()
        test_driver.Pandas = True
        test_driver.Limit = 30
        test_driver.Profile_full = True
        try:
            twint.run.Search(test_driver)
        except Exception as error_fetching:
            logging.exception(f"Error fetching data from twitter [{error_fetching}]!\n" +
                            "Does the user have their tweets viewable?")

        output = twint.storage.panda.Tweets_df
        logging.info(f">>>>>>>>>>\n{output}\n")

        if len(output) < 1:
            logging.error(f"ERROR >> {output}")
            free_bot.set_status(3)
            return []
        fin_output = get_normal_tweet(df=output, num=free_bot.get_num_tweets())

    if not fin_output:
        logging.warning("No tweets found, returning...")
        return fin_output

    logging.info(f"function get_tweet is returning \n{fin_output}")
    free_bot.set_tweets(fin_output)
    return fin_output

def check_if_user_exists(username) -> bool:
    """
    Checks if user exists by running twint on given username

    :param username: Name to check
    """
    try:
        user_check = twint.Config()
        user_check.Hide_output = True
        user_check.Username = username
        user_check.Limit = 1
        twint.run.Search(user_check)
    except Exception as user_find_error:
        logging.exception(f"USER DOES NOT EXIST {user_find_error}")
        return False
    logging.info("USER DOES EXIST")
    return True

def get_normal_tweet(df: pandas.DataFrame, num: int = 1) -> list[str]:
    """
        While the current number of grabbed pictures doesn't exceed the num
        OR
        While the current index isn't greater than the length of the list
    """
    num_of_tweets: int = 0
    tweets = []
    for i in range(len(df)):
        logging.info(tweets)
        if num_of_tweets >= num:
            break
        logging.info(f"ADDING: {tweets}")
        tweets.append(link_conversion.fix_links(df.loc[i].link))
        num_of_tweets = num_of_tweets + 1
    logging.info(f"List of tweets gotten {tweets}")
    return tweets

def get_single_missing(username: str) -> list[str]:
    """
    Function returns the 10 most recent tweets, IDs only
    """
    
    num = 10
    new_list: list[str] = []
    missing_data = extra_data.pull_and_process_data(username, num)

    all_links = missing_data.get_all_ids()
    all_links.sort(reverse=True)
    
    if not all_links:
        return new_list

    # new_list = [(f"https://fxtwitter.com/{username}/status/{x}") for x in all_links]
    # print("TEMP>" + new_list)
    return all_links

def get_missing_tweets(free_bot: FreeBot) -> list[str]:
    """
    Function gets the tweets that are usually missed by twint.

    :param free_bot: Stores 
    :param num_tweets: Number of tweets to go back and grab
    :param missing_data: A_data class containing data fetched from nitter
    :param new_list: List of links to be returned

    :returns: List of tweets
    """
    new_list: list[str] = []
    missing_data = extra_data.pull_and_process_data(free_bot.get_username(), free_bot.get_num_tweets())
    logging.debug(f"All current links in get_missing_tweetsDid we get all data? ->{missing_data.got_all_requested}\n{missing_data.get_all_ids()}")

    all_links = missing_data.get_all_ids()
    all_links.sort(reverse=True)
    
    logging.debug(f"WE GOT >>>> {all_links}")
    if not missing_data.get_all_req():
        logging.warning(f"WE ONLY HAVE {len(all_links)} LINKS BUT REQUESTED {free_bot.get_num_tweets()}")

    # FUTURE NOTE: CHANGE FUNCTION TO RETURN TUPLE WITH A STATUS CODE
    if not all_links:
        return new_list

    new_list = [(f"https://fxtwitter.com/{free_bot.get_username()}/status/{x}") for x in all_links]
    print(new_list)
    return new_list[:free_bot.get_num_tweets()]

if __name__ == "__main__":
    os.exit(0)
