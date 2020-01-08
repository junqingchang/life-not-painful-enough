import praw
import json
import pandas as pd


def scrapper(client_id, client_secret, user_agent, num_post=10, outfile='scrape_results.csv'):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    roast_posts = reddit.subreddit('RoastMe').hot(limit=num_post)
    idx = 0
    posts = []
    for post in roast_posts:
        if idx < 2:
            idx += 1
            continue
        title = post.title
        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=0)
        count = 0
        for top_level_comment in submission.comments:
            comment = top_level_comment.body
            posts.append([title, comment])
            count += 1
            if count > 500:
                break
    posts = pd.DataFrame(posts,columns=['title', 'comment'])
    posts.to_csv(outfile)

if __name__ == '__main__':
    with open('.env') as f:
        config = json.load(f)
    scrapper(config['client_id'], config['client_secret'], config['user_agent'], 5000)