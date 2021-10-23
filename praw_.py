async def praw_login(post):
    import asyncpraw as praw
    import urllib
    import urllib.request
    import json        
    
    filename = ('image.png')
    found = False
    with open("config.json") as f:
        config = json.load(f)
    reddit = praw.Reddit(client_id='oVD8qBhq5Ab3Wg',
                        client_secret=config["praw_secret"], password=config["praw_password"],
                        user_agent='Rtheif', username="Mr_Turbotylar")
    sent = []
    try:
            with open("sent.json", "r") as f:
                sent = json.load(f)
    except:
            pass
    while not found:
                subreddit = await reddit.subreddit(post)
                async for submission in subreddit.hot():
                    if submission.permalink in sent:
                        continue
                    url = (submission.url)
                    sent.append(submission.permalink)
                    with open("sent.json", "w") as f:
                        json.dump(sent, f)
                    if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
                        urllib.request.urlretrieve(url, filename)                        
                        found = True
                        break