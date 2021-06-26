# nfl_sentiment_analysis
Sentiment Analysis of [r/nfl](https://www.reddit.com/r/nfl/) live-streamed comments

## Intro
This program uses the Reddit API to receive r/nfl comments in real time.  It then performs sentiment analysis on each user comment.  Results are then emitted from the server back to the web browser via the socket.io JS / Python library. A [Reddit API account](https://www.reddit.com/dev/api/) is needed in order to fetch the user comments.

This is just an experiment to learn more about:

* [socket.io](https://socket.io/) - for both JS and Python versions
* The [Asynchronous Python Reddit API Wrapper](https://github.com/praw-dev/asyncpraw)
* The [TextBlob: Simplified Text Processing](https://textblob.readthedocs.io/) library to perform [Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis)
* The [Uvicorn](https://www.uvicorn.org/) ASGI server
* The Python 3 [async / await](https://docs.python.org/3/library/asyncio-task.html) library
