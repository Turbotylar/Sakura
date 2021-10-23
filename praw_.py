def praw_login(subreddit):
    import praw
    import urllib
    import urllib.request
    import json

    
    with open("config.json") as f:
        config = json.load(f)

    filename = ('image.png')
    found = False
    
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

        

            for post in reddit.subreddit(subreddit).hot():
                if post.permalink in sent:
                    #print("Scam")
                    continue
            
                url = (post.url)

                sent.append(post.permalink)

                with open("sent.json", "w") as f:
                    json.dump(sent, f)
                
                
                if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
                    #print("Saved")
                    urllib.request.urlretrieve(url, filename)
                    found = True
                    break
    #print("Done.")
