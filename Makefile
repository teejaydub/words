run:
	pipenv run ./search.py

test:
	pipenv run ./search.py --test

depends:
	pip install --user pipenv
	pipenv install
	pipenv shell
