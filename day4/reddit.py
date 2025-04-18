import praw

class RedditTool:
    def __init__(self):
        # init bot
        self.reddit = praw.Reddit('newsbot')
        # init subreddits
        self.subreddits = {
            'r_news' : self.reddit.subreddit("news"),
            'r_worldnews' : self.reddit.subreddit("worldnews"),
            'r_nottheonion' : self.reddit.subreddit("nottheonion"),
            'r_thescoop' : self.reddit.subreddit("thescoop")
        }
        
    def getHot(self, sub_name='r_news', lim=5):
        ret = []
        for submission in self.subreddits[sub_name].hot(limit=lim):
            ret.append({
                'title': submission.title,
                'text': submission.selftext,
                'score': submission.score,
                'url': submission.url
            })
        return ret
            
    def getTop(self, sub_name='r_news', lim=5):
        ret = []
        for submission in self.subreddits[sub_name].top(limit=lim):
            ret.append({
                'title': submission.title,
                'text': submission.selftext,
                'score': submission.score,
                'url': submission.url
            })
        return ret
            
    def getNew(self, sub_name='r_news', lim=5):
        ret = []
        for submission in self.subreddits[sub_name].new(limit=lim):
            ret.append({
                'title': submission.title,
                'text': submission.selftext,
                'score': submission.score,
                'url': submission.url
            })
        return ret
            
    def getRising(self, sub_name='r_news', lim=5):
        ret = []
        for submission in self.subreddits[sub_name].rising(limit=lim):
            ret.append({
                'title': submission.title,
                'text': submission.selftext,
                'score': submission.score,
                'url': submission.url
            })
        return ret
