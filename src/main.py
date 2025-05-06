import os
import time

from instaloader import Instaloader, Profile

import config

loader = Instaloader()

if os.path.exists(f"session-{config.USERNAME}"):
    loader.load_session_from_file(f"session-{config.USERNAME}")
else:
    loader.login(config.USERNAME, config.PASSWORD)
    loader.save_session_to_file(filename=f"session-{config.USERNAME}")

profile = Profile.from_username(loader.context, config.PROFILE)

followers = profile.get_followers()  # Saves the Original Followers Number.

while True:
    current_followers = profile.get_followers()

    if len(current_followers) < len(followers):
        unfollowers = list(set(followers) - set(current_followers))
        print(f"User/s unfollowed you: {unfollowers}")
    if len(current_followers) > len(followers):
        followers = current_followers

    time.sleep(60 * 15)
