
APP = basicapp

test:
	python manage.py test -v2 $(APP)
