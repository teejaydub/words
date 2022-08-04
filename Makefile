run:
	python search.py

test:
	python search.py --test

depends:
	pip install --user pipenv
	pipenv install
	pipenv shell
