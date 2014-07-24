import praw
from config import config
import sqlite3 as lite
import sys

class Bot(object):



    def __init__(self):
        self.r = praw.Reddit(user_agent=config['user_agent'])

    def get_comments_for_user(self,user_name):
        # this fuction returns all the comments for a user
        reddit_user = self.r.get_redditor(user_name)
        comments = reddit_user.get_comments()
        return comments

    def get_comments_for_all(self):
        #this function returns all the comments on the first
        #page of reddit
        comments = self.r.get_comments('all')
        return comments

    def run(self, comment_context):

        swear_words = ['fuck', 'shit', 'bitch', 'cunt', 'asshole']

        self.r.login(config['username'], config['password'])

        # get comments
        if comment_context == 'all':
            comments = self.get_comments_for_all()
        else:
            comments = self.get_comments_for_user(comment_context)



        # Get comments for testing
        for comment in comments:
            if any(s in comment.body.lower() for s in swear_words):
                user = comment.author
                swear_comment = comment.body
                print "This dude swore: %s" % user

                # Connect to DB
                con = lite.connect('test_sinners.db')
                #with con:
                cur = con.cursor()
                cur.execute('INSERT INTO comments VALUES(NULL,"{0}","{1}",0)'.format(user, swear_comment))

                cur.execute('SELECT COUNT(*) FROM comments WHERE user = "{}"'.format(user))
                con.commit()
                swear_count = cur.fetchone()[0]

                if swear_count <= 1:
                    print "New user: %s" % user

                    # comment.reply('You just swore! Repent for your sins at [swearjarbot.com](swearjarbot.com/?user=%s).') % author


                ### User exists, need to update ###
                else:
                    print "Existing user: %s \nOld swear count: %s" % (author, swear_count)

                    # comment.reply('You just swore! I've caught you %s times. Repent for your sins at [swearjarbot.com](swearjarbot.com/?user=%s).') % (swear_count, author)


                # Close connection - Not sure when the fuck to close this connection.
                #    con.close()

if __name__ == '__main__':



    try: 
        sys.argv[1]    
    except IndexError:
        print "you're a tard muffin"
    else:
        b = Bot()
        b.run(sys.argv[1])

