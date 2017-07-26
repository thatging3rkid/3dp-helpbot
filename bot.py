"""
/r/3DPrinting Help Bot
Tries to help users by replying to them with helpful links

:author: Connor Henley, @thatging3rkid
"""
import time
import praw
import praw.models

import config

version = "v0.1"

DEBUG_INFO = "\n\n*****\nI am a bot | /r/3DPrinting Help Bot by " \
             "[/u/thatging3rkid](https://reddit.com/user/thatging3rkid) " + version + " | Report bugs [here]" \
             "(https://reddit.com/r/3dprinting_helpbot) | [GitHub](https://github.com/thatging3rkid/3dp-helpbot)"
KEYWORDS = ["3d modeling program", "cad program", "looking for cad program", "looking for modeling program",
            "3d modeling software"]

# A class isn't necessary, but globals in Python are weird
class Bot:

    __slots__ = ["__viewed", "__bot"]

    def __init__(self):
        # Login
        self.__bot = praw.Reddit(username=config.username, password=config.password, client_id=config.client_id,
                          client_secret=config.client_secret, user_agent="3dprinting_helpbot " + version)

        # Initialize data
        self.__viewed = []

        # Run the bot
        while True:
            self.__run()

            if len(self.__viewed) > 100:
                for i in range(0, 10):
                    self.__viewed.remove(0)
        pass

    def __run(self):
        """
        Checks for new posts and replies
        """

        # Get new posts
        for post in self.__bot.subreddit('3dprinting_helpbot').new(limit = 10):
            # Only check the post once
            if post.id not in self.__viewed:
                self.__viewed.append(post.id)

                # See if a post needs a reply
                for word in KEYWORDS:
                    if word in post.title.lower() or word in post.selftext.lower():
                        post.reply("[Here](https://www.reddit.com/r/3Dprinting/wiki/index#wiki_what_should_i_do_to_start_modelling_things_to_print.3F)"
                                   " is a list of CAD/3D modeling software" + DEBUG_INFO)
                        break
            pass

        # Read the inbox for mentions and replies
        read = []
        for item in self.__bot.inbox.unread(limit = 25):
            if isinstance(item, praw.models.Comment):
                # Mark as read
                read.append(item)

                # Check the contents of the inbox item
                if "/u/3dprinting_helpbot modeling" in item.body.lower():
                    # Bot has been summoned, give out info
                    item.reply("[Here](https://www.reddit.com/r/3Dprinting/wiki/index#wiki_what_should_i_do_to_start_modelling_things_to_print.3F)"
                        " is a list of CAD/3D modeling software" + DEBUG_INFO)
                elif "good bot" == item.body.lower().strip():
                    # Someone called the bot a good bot!
                    item.reply("Thanks!" + DEBUG_INFO)
                elif "bad bot" == item.body.lower().strip():
                    # Oh no, the bot did something bad. Feedback is welcome!
                    item.reply("I'm sorry to hear that. You can leave feedback [here](https://reddit.com/r/3dprinting_helpbot)." + DEBUG_INFO)
        self.__bot.inbox.mark_read(read)

        time.sleep(2) # Conform to Reddit's API; reduce spam and processing load
    pass

def main():
    Bot()

main()