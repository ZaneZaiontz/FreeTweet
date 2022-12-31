"""
    This file handles scriping twitter data and planning for future uses. The main purpose of this is to pull data from creators to be 
    posted to a discord channel and update the users who requested it.
    
    NOTES:
        - Use Twint to get tweet data, as it uses the 'unofficial' Twitter API, which saves on personal WS
    
    Future features:
        - Ability to follow creators
        - Ability to unfollow creators
        - Auto-update for Twitter timeline
            - Ability to filter what types of tweets are posted by the bot (such as only images, only replies, etc.)
        - Upon following, ability to post the last X number of posts (most likely will have a 5 tweet limit to start)
        - Set auto-update frequency (For now with a min time of every 5 minutes)
        - Ability to check tweet record and ONLY post new posts that the bot has yet to post
        - Flags set per creator, such as if the work should be posted with a spoiler tag
        - Ability to scan tweet and alert server/users depending on what the tweet says
            - EX: If you're looking for the words "comissions open!", the bot will @ the user(s) who want to be notified
        - POSSIBLE Api setup that can be sent user data and get only what's needed
        
    TODO:
        - Document code corrently
        - Add correct types
        - Finish adding correct functionality for main loop
        - Clean everything up, god it looks horrible 
        - Please 
        - Additional features
"""
import twint
import discord
import pandas
from processing import link_conversion
import asyncio
from asyncio import get_event_loop, TimeoutError, ensure_future, new_event_loop, set_event_loop
import nest_asyncio


class FreeBot:
    def __init__(self):
        self.TOKEN = open("../data/auth.txt", "r").readline()
        

def temp_get_tweet(message:str="khyleri", num_tweets:int = 1) -> str:
    test_driver = twint.Config()
    test_driver.Hide_output = True
    test_driver.Username = message
    test_driver.Pandas = True
    test_driver.Limit = 5
    twint.run.Search(test_driver)
    output = twint.storage.panda.Tweets_df
    
    # for i in range(num_tweets):

    link_part = output.loc[0].link
    print(f"GOT\n{link_part}")
    link_fixed = link_conversion.fix_links(link_part)
    print(link_fixed)
    return link_fixed

def run_bot():
    """
        TODO
    """
    freeBot = FreeBot()
    intent = discord.Intents.default()
    intent.message_content = True
    client = discord.Client(intents=intent)
    
    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f"{username} said: '{user_message}' ({channel})")
        
        if user_message[0] == '>':
            try:
                user_message = user_message[1:]
                message_tokens = user_message.split()
                if message_tokens[0] == "get-tweet":
                    print(message_tokens[1])
                    link = temp_get_tweet(message_tokens[1])
                    await send_message(message, link, is_private=False, is_tweet=True)
                else:
                    await send_message(message, user_message, is_private=False, is_tweet=True)
            except Exception as e:
                print(e)
                await send_message(message, user_message, is_private=False, is_tweet=True)
        elif user_message[0] == '-':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
    
    client.run(freeBot.TOKEN)

def scrape_driver():
    """
        TODO
    """
    test_driver = twint.Config()
    test_driver.Username = "khyleri"
    test_driver.Limit = 5
    test_driver.Output = "tweets.csv"
    test_driver.User_full = True
    twint.run.Search(test_driver)

async def send_message(message, user_message, is_private, is_tweet = False):
    """
        TODO
    """
    if is_tweet:
        try:
            await message.channel.send(user_message)
        except Exception as e:
            print(e)
        pass
    else:
        try:
            response = get_response(user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
            print(e)

def get_detailed_response(message: str) -> str:
    """
    TODO
    
    Args:
        message (str): _description_

    Returns:
        str: _description_
    """
    message_tok = message.split()
    
    match len(message_tok):
        case 0:
            pass
        case 1:
            print(f"ONLY SUPPLIED {message_tok[0]}, NEED MORE DATA")
        case 2:
            pass
        case 3:
            pass
        case default:
            pass
    
    

def get_response(message: str) -> str:
    """
        Old responces, will be changed out for get_detailed_response in future version
    """
    l_message = message.lower()
    
    if l_message == "test":
        return "Got it!"

if __name__ == "__main__":
    nest_asyncio.apply()
    run_bot()