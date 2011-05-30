
APP = basicapp

test:
	python manage.py test --settings=test_settings $(APP)

pep8:
	pep8 --statistics --show-pep8 --filename=*.py ./

pyflakes:
	pyflakes .
