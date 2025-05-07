import os
import time

import instaloader

USERNAME = input("Enter your Username: ")
PASSWORD = input("Enter your Password: ")
PROFILE = input("Enter the Profile Username you want to watch: ")
session = f"session-{USERNAME}"

loader = instaloader.Instaloader()

loader.context._session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
})

if os.path.exists(session):
    loader.load_session_from_file(username=USERNAME, filename=session)
else:
    try:
        loader.login(USERNAME, PASSWORD)
        loader.save_session_to_file(filename=f"{session}")
    except instaloader.InstaloaderException as e:
        print(f"Exception: {e}")
        for i in range(5, 0, -1):
            print(f"waiting {i} seconds", end="\r")
            time.sleep(1)
        exit(1)

print("Waiting a Minute so we don't hit Instagram limit rate")
time.sleep(60)

try:
    profile = instaloader.Profile.from_username(loader.context, PROFILE)
    followers = profile.get_followers()  # Saves the Original Followers Number.
except instaloader.InstaloaderException as e:
    print(f"Exception: {e}")
    for i in range(5, 0, -1):
        print(f"waiting {i} seconds", end="\r", flush=True)
        time.sleep(1)
    exit(1)

while True:
    try:
        current_followers = profile.get_followers()

        if len(current_followers) < len(followers):
            unfollowers = list(set(followers) - set(current_followers))
            print(f"User/s unfollowed you: {unfollowers}")
        if len(current_followers) > len(followers):
            followers = current_followers

    except instaloader.InstaloaderException as e:
        print(f"Exception: {e}\n Trying again after 15 Mins")

    time.sleep(60 * 15)
