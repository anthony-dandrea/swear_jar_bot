swear_jar_bot
=============

### Dependencies

* `pip`
* `virtualenv`
* `python 2.7.6`

### Before you Run

Need to make a sinner.db before running main.py
  * Using Reddit username for keyvalue and INT to keep track of the user's swears.
  * The web app will interact with this database as well. (more info on seeding DB later...)

### Run

`make run`

### To-Do

1. Make the flask web app that will interact with sinner.db.

2. Single page app that uses ajax to call in the user's swear count based on user name. Hopefully username can be added to the url so the bot can put links in comments that will link to that specific users swear count on page load.

3. This seems like the best option so far for actually donating money to charities - [First Giving](http://developers.firstgiving.com/)
  * I'm thinking the hard part will be trying to lower the swear count in the db after there is money donated. Haven't used their API yet so not sure if they make it easy or not.

