run:
	python search.py

test:
	python search.py --test

depends:
	pipenv install
	pipenv shell
