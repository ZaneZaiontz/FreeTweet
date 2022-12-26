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
"""
import twint

def scrape_driver():
    """
        TODO
    """
    pass

if __name__ == "__main__":
    scrape_driver()