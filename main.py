import praw
from config import config
import sqlite3 as lite
import sys


def main():

	swear_words = ['fuck', 'shit', 'bitch', 'cunt', 'asshole']

	r = praw.Reddit(user_agent=config['user_agent'])
	r.login(config['username'], config['password'])

	# Get all comments
	all_comments = r.get_comments('all')


	# Get comments for testing
	for comment in all_comments:
		print comment
		if any(s in comment.body.lower() for s in swear_words):
			author = comment.author
			print "This dude swore: %s" % author


			# Connect to DB
			con = lite.connect('sinners.db')
			with con:
				cur = con.cursor()
				cur.execute('''SELECT Count FROM Sinners WHERE User=?''', (author,))


				### User doesn't exist ###
				swear_count = cur.fetchone()
				if swear_count is None:
					print "New user: %s" % author
					
					# Add this new sinner to santa's naughty list
					cur.execute("INSERT INTO Sinners VALUES(?,?)", (author,1))

					# comment.reply('')


				### User exists, need to update ###
				else:
					print "Existing user: %s \nOld swear count: %s" % (author, swear_count)

					swear_count = swear_count[0] + 1
					print "After swear count %s" % swear_count

					# Tack another one on for this guy
					cur.execute("UPDATE Sinners SET Count=? WHERE User=?", (swear_count, author))

					# comment.reply('You swore %s time(s). Pay for your sins by going to http://swearjar.com' % swear_count)


				# Close connection - Not sure when the fuck to close this connection.
				con.close()

if __name__ == '__main__':
	main()
