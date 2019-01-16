"""
/r/3DPrinting Help Bot
Tries to help users by replying to them with helpful links

:author: Connor Henley, @thatging3rkid
"""
import os
import sys
import time
import pickle
import praw
import praw.models
import datetime
import traceback
import subprocess

import config


version = ""
try:
    version = subprocess.check_output(["git", "describe", "--tags"]).strip().decode("utf-8")
except:
    version = "unknown"

DEBUG_INFO = "\n\n*****\nI am a bot | /r/3DPrinting Help Bot by " \
             "[/u/thatging3rkid](https://reddit.com/user/thatging3rkid) | version " + version + \
             " | [GitHub](https://github.com/thatging3rkid/3dp-helpbot)"

KEYWORDS = ["3d modeling program", "cad program", "cad software", "looking for modeling program",
            "3d modeling software", "software for designing 3d models", "software to make 3d models",
            "software for 3d modeling", "3d modelling program", "3d editing software", "3d editing program"]


# A class isn't necessary, but globals in Python are weird
class Bot:

    def __init__(self):
        # Login
        self.__bot = praw.Reddit(username=config.username, password=config.password, client_id=config.client_id,
                          client_secret=config.client_secret, user_agent="3dprinting_helpbot " + version)
        print("Logged in...")

        # Initialize data
        try:
            df = open("data.dat", "rb")
            self.__viewed = pickle.load(df)
            df.close()
        except:
            self.__viewed = []

        # Run the bot
        i = 0
        while True:
            try:
                self.__run()

                if len(self.__viewed) > 200:
                    for i in range(0, 15):
                        self.__viewed.remove(0)

                # Write the viewed ids to disk every 5 iterations
                if i == 5:
                    i = 0
                    df = open("data.dat", "wb")
                    pickle.dump(self.__viewed, df)
                    df.close()
                else:
                    i += 1
            except Exception:
                traceback.print_exc()
        pass

    def __run(self):
        """
        Checks for new posts and replies
        """

        # Get new posts
        for post in self.__bot.subreddit('3dprinting').new(limit = 20):
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

        time.sleep(6)  # Conform to Reddit's API; reduce spam and processing load
    pass

def main():
    print("Starting /u/3dprinting_helpbot...")
    Bot()

os.chdir("/home/user/3dp-helpbot")
sys.stdout = open("logs/log-" + datetime.datetime.now().strftime("%m-%d-%Y_%X") + ".txt", "w+")
sys.stderr = sys.stdout
main()
