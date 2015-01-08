PYTHON = $(shell which python2.7)
ENV = $(CURDIR)/env

virtual-env:
	virtualenv --python=$(PYTHON) $(ENV)

env: virtual-env
	$(ENV)/bin/pip install -r requirements.txt

run_bot: 
	$(ENV)/bin/python main.py all

run_app:
	$(ENV)/bin/python app.py

run_bot_user:
	$(ENV)/bin/python main.py $(USERNAME)

wsgi:
	$(ENV)/bin/uwsgi --socket 127.0.0.1:8080 -w WSGI:app

clean:
	rm -rf $(ENV)
