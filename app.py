
r"""
app.py
-John Taylor
June-26-2021

Sentiment Analysis of r/nfl live-streamed comments
https://github.com/jftuga/nfl_sentiment_analysis

Copy creds--TEMPLATE.py to creds.py and then modify accordingly

This requires uvicorn to run: https://www.uvicorn.org/
Instantiation : uvicorn --reload --no-use-colors app:app

"""

import asyncpraw
import socketio
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer

from creds import reddit_client_id, reddit_client_secret, project_url, project_author

project_version = "1.0.0"
project_name = "NFL Sentiment Analysis"
user_agent = f"{project_url} v{project_version} by {project_author}"


###

# Sentiment Analysis
class StAn:
    def __init__(self):
        self.sentiment_1 = ""
        self.sentiment_2 = ""

    def get_comment_sentiment_1(self, comment: str):
        analyzer = PatternAnalyzer()
        pattern_analysis = TextBlob(comment, analyzer=analyzer)
        sentiment = pattern_analysis.sentiment
        pol = sentiment.polarity
        sub = sentiment.subjectivity
        self.sentiment_1 = f"{pol:.2f}, {sub:.2f}"

    def get_comment_sentiment_2(self, comment):
        analyzer = NaiveBayesAnalyzer()
        result = TextBlob(comment, analyzer=analyzer)
        pos = result.sentiment.p_pos
        neg = result.sentiment.p_neg
        diff = pos - neg
        self.sentiment_2 = f"{diff:.2f}, {pos:.2f}, {neg:.2f}"

    def analyze(self, comment: str) -> tuple:
        self.get_comment_sentiment_1(comment)
        self.get_comment_sentiment_2(comment)
        return self.sentiment_1, self.sentiment_2


###

# AsyncPraw
class AsPr:
    def __init__(self, sr: str):
        self.sr = sr  # subreddit
        self.reddit = asyncpraw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret,
                                       user_agent=user_agent)
        self.sentiment = StAn()

    async def close(self):
        await self.reddit.close()

    async def stream(self):
        subreddit = await self.reddit.subreddit(self.sr)
        async for submission in subreddit.hot(limit=3):
            print(f"{submission.id} {submission.title}")
        print()

    async def all_comments(self, sio, sid):
        max_comment_length = 225
        subreddit = await self.reddit.subreddit(self.sr)
        async for comment in subreddit.stream.comments():
            if len(comment.body) < 4:
                continue
            sa1, sa2 = self.sentiment.analyze(comment.body[:max_comment_length])
            if not comment.author_flair_text:
                slim_flair = ""
            elif len(comment.author_flair_text) < 4:
                slim_flair = ""
            elif comment.author_flair_text.count(":") >= 2:
                slim_flair = comment.author_flair_text.split(":")[1]
            else:
                slim_flair = comment.author_flair_text
            result = {"comment": comment.body[:max_comment_length], "flair": slim_flair, "sa1": sa1, "sa2": sa2}
            await sio.emit("comment", result, to=sid)


###

# Main
sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(sio, static_files={
    '/': './public/'
})


async def main(sio_obj, sid):
    aspr = AsPr("nfl")
    await aspr.all_comments(sio_obj, sid)
    await aspr.close()


@sio.event
async def reddit(sid):
    await main(sio, sid)
