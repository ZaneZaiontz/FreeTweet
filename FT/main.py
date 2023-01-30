"""Main file to run the bot"""
import time
import logging
import discord
import asyncio
import threading
import nest_asyncio
import bot.tweet_scrape as scrapper
# from discord.ext import commands
from bot.processing.link_data import AUTH
from bot.processing import link_conversion

TWT_NUM = 1

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class FreeBot:
    """ Class for controling data for FreeTweet """

    def __init__(self):
        """
        Constructor

        :param TOKEN: Bot token needed for actually running bot
        :param followed_users: List of users being followed by the bot, needs to be read in
        :param bot_db: DB associated with the bot, should store IDs and usernames at a minimum
        :param allow_adult: Bool, if the user wants to see 18+ content
        :param symbol: Symbol typed into discord to access the bot
        """
        self.TOKEN: str = AUTH
        self.followed_users: list[str] = [] #GET_USERS() This should be moved to a database
        self.symbol: chr = '!' #GET_SYMBOL()
        self.tweets: list[str] = [] # maybe change this to a set?
        self.status_code: int = 0
        self.fetch_additional: bool = False
        self.num_of_tweets: int = 1
        self.username: str = "khyleri"
        self.spoiler: bool = False

    def get_follows(self) -> list[str]:
        """ Gets list of followers the bot is currently following"""
        return self.followed_users

    def get_symbol(self) -> chr:
        """ Gets the symbol used for commands with the bot """
        return self.symbol

    def get_tweets(self) -> list[str]:
        """
        Gets a list of all tweets grabbed by the bot
        NOT CURRENTLY USED
        """
        return self.tweets

    def get_status(self) -> int:
        """ Gets the current status code """
        return self.status_code

    def get_additional(self) -> bool:
        """ Gets bool if extra data is being pulled """
        return self.fetch_additional

    def get_num_tweets(self) -> int:
        """ Gets number of tweets to pull """
        return self.num_of_tweets

    def get_username(self) -> str:
        """ Gets the current username being looked up """
        return self.username

    def get_spoiler(self) -> bool:
        """ Gets the current status if tweets need to be spoilered """
        return self.spoiler

    def add_follower(self, user: str) -> None:
        """
        Adds an additional user to the follower list
        FUTURE FEATURE
        """
        if scrapper.check_if_user_exists(user):
            self.followed_users.append(user)

    def set_symbol(self, symbol: chr) -> None:
        """ Sets new custom symbol to be used to call the bot """
        self.symbol = symbol

    def add_tweet(self, tweet: str) -> None:
        """ Adds a single tweet to the list of tweets"""
        self.tweets.append(tweet)

    def set_tweets(self, tweets: list[str]) -> None:
        """ Different from add_tweet, replaces current list of tweets with new one"""
        self.tweets = tweets

    def set_status(self, num: int) -> None:
        """ Sets the status code """
        self.status_code = num

    def set_additional(self, fetch: bool) -> None:
        """ Sets flag for if extra data should be grabbed"""
        self.fetch_additional = fetch

    def set_num_of_tweets(self, num: int) -> None:
        """ Sets the number of tweets to look for"""
        self.num_of_tweets = num

    def set_username(self, user: str) -> None:
        """ Sets the username to grab tweets from """
        self.username = user

    def set_spoiler(self, spoil: bool) -> None:
        """ Sets flag for if output should have discord spoilers"""
        self.spoiler = spoil

def run_bot(free_bot: FreeBot) -> None:
    """
    Runs the main bot.

    :param free_bot:
    :param intent:
    :param client:
    """
    intent = discord.Intents.default()
    intent.message_content = True
    client = discord.Client(intents=intent)

    @client.event
    async def on_ready():
        logging.info(f"{client.user} is now running!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        logging.info(f"{username} said: '{user_message}' ({channel})")
        logging.info(f"{str(message)}")
        if user_message[0] == free_bot.get_symbol():
            await handle_user_message(message, user_message, free_bot)
    client.run(free_bot.TOKEN)

async def handle_user_message(message: discord.message.Message,
                              user_message: str,
                              free_bot: FreeBot) -> None:
    """
    Checks the users input then processes it depending on the message

    :param message:
    :param user_message:
    :param free_bot:
    :param links:
    :param status_code:

    :returns: None

    Example:
        !get-tweet user 15 nsfw
    """

    links: list = []
    try:
        if len(user_message) <= 1:
            free_bot.set_status(0)
            await format_response(message, free_bot)
            return

        user_message = user_message[1:]
        message_tokens = user_message.split()

        if str(message_tokens[0]) == "get-tweet":
            await handle_get_tweet(message, message_tokens, free_bot)
        elif message_tokens[0] == "help":
            free_bot.set_status(1)
            await format_response(message, free_bot)
        elif message_tokens[0] == "follow":
            await handle_following(message, message_tokens[1], free_bot)
            await send_message(message, "TESTING FOLLOW")
        else:
            free_bot.set_status(4)
            await format_response(message, free_bot)
    except Exception as tok_error:
        logging.error(f"Error with user message: {tok_error}")
        free_bot.set_status(0)
        await format_response(message, free_bot)
    

async def handle_get_tweet(message, message_tokens: list, free_bot: FreeBot) -> None:
    """
    Functions handles the get_tweet

    :returns: Tuple containing a list and an int acting as a status code
    """
    links = []
    logging.info(f"TOK LEN {len(message_tokens)}\n{message_tokens}")
    
    if len(message_tokens) <= 1:
        free_bot.set_status(4)
        return

    if not scrapper.check_if_user_exists(message_tokens[1]):
        free_bot.set_status(2)
        return

    free_bot.set_username(message_tokens[1])
    match len(message_tokens):
        case 2:
            free_bot.set_additional(False)
            free_bot.set_num_of_tweets(TWT_NUM)
        case 3:
            if message_tokens[2].isdigit():
                free_bot.set_num_of_tweets(int(message_tokens[2]))
                free_bot.set_additional(False)
            elif message_tokens[2] == "nsfw":
                free_bot.set_additional(True)
                free_bot.set_num_of_tweets(TWT_NUM)
        case 4:
            if message_tokens[2].isdigit() and message_tokens[3] == "nsfw":
                free_bot.set_num_of_tweets(int(message_tokens[2]))
                free_bot.set_additional(True)
    links = scrapper.get_tweet(free_bot)
    if not links:
        await format_response(message, free_bot)
    else:
        for link in links:
            await send_message(message, link)

async def handle_following(message, username, free_bot):
    free_bot.add_follower(username)
    pass

async def send_message(message, user_message) -> None: # is_private
    """
    Sends a messageto the discord channel
    Currently does not support direct messaging a user

    :prarm message:
    :prarm user_message:
    """
    try:
        await message.channel.send(user_message)
    except Exception as e:
        logging.error(f"ERROR ENDING MESSAGE: {e}")

async def format_response(
    message: discord.message.Message,
    free_bot: FreeBot):
    """
        Create codes to pick and choose errors

        -99 to -1 - General error
        0 - Normal status, no error
        1 - Displays help message
        2 - Missing account
        3 - No tweets from account
        4 - Incorrect format
        5 - Banned account
    """
    error_message = str(
                          ">>> **Error**\n"
                        + "__Something went wrong__\n"
                        + f"Use {free_bot.get_symbol()}help for help\n"
    )

    help_message = str(
                          ">>> **Help**\n"
                        + "__Formatting__\n"
                        + f"`All commands must start with {free_bot.get_symbol()}`\n\n" 
                        + "**Available commands**\n"
                        + "__help__\n"
                        + "*Example*\n"
                        + f"`{free_bot.get_symbol()}help`\n\n"
                        + "__get-tweet__\n"
                        + "*Example*\n"
                        + f"`{free_bot.get_symbol()}get-tweet khyleri`\n"
                        + f"`{free_bot.get_symbol()}get-tweet khyleri 5`\n"
                        + f"`{free_bot.get_symbol()}get-tweet khyleri nsfw`\n"
                        + f"`{free_bot.get_symbol()}get-tweet khyleri 5 nsfw`\n"
            )

    no_account_message = str(
                          ">>> **ACCOUNT NOT FOUND**\n"
                        + "*Please check to make sure you've entered the account name correctly*\n"
    )

    formatting_message = str (
        f"Error, incorrect format:\nUse `{free_bot.symbol}help` for help formatting"
    )

    no_tweets_found = str (
                        ">>> **PLACEHOLDER**\n"
                        "*REQUESTED ACCOUNT EXISTS, BUT NO TWEETS WERE FOUND TO PULL*\n"
    )

    match free_bot.get_status():
        case 0:
            await send_message(message, "No error, placeholder for now")
        case 1:
            await send_message(message, help_message)
        case 2:
            await send_message(message, no_account_message)
        case 3:
            await send_message(message, no_tweets_found)
        case 4:
            await send_message(message, formatting_message)
        case default:
            await send_message(message, error_message)

# async def check_for_tweets(free_bot):
#     """
#     Threaded - checks for new follows
#     """
#     temp_tweet_dict: dict = {}
#     while True:
#         time.sleep(10)
#         if free_bot.get_follows():
#             follows = free_bot.get_follows()
#             print(f"FOUND FOLLOWERS {follows}")
#             for follow in follows:
#                 if follow in temp_tweet_dict:
#                     tmp = scrapper.get_tweet(free_bot)
#                     for tp in tmp:
#                         if tp not in temp_tweet_dict[follow]:
#                             #send message
#                             pass
#                 else:
#                     temp_tweet_dict[follow] = scrapper.get_tweet(free_bot)
    
if __name__ == '__main__':
    nest_asyncio.apply()
    free_bot = FreeBot()
    
    # main_thread = threading.thread(target=run_bot, args=(free_bot))
    # main_thread.start()
    
    # sub_thread = threading.Thread(target=asyncio.run, args=(check_for_tweets(free_bot),), daemon=True)
    # sub_thread.start()
    run_bot(free_bot)
    