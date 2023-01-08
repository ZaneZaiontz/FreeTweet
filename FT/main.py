import nest_asyncio
import bot.tweet_scrape

def main():
    nest_asyncio.apply()
    bot.tweet_scrape.run_bot()

if __name__ == '__main__':
    main()