import praw
# from pprint import pprint
from config import config

swear_words = ['fuck', 'shit', 'bitch', 'cunt', 'asshole']

r = praw.Reddit(user_agent=config['user_agent'])
r.login(config['username'], config['password'])

# get all comments
all_comments = r.get_comments('all')

# get comments for testing
for comment in all_comments:
	print comment
	if any(s in comment.body.lower() for s in swear_words):
		print 'swear found!!!'
