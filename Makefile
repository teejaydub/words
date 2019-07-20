run:
	python search.py

test:
	python search.py --test

depends:
	conda env create
	conda activate words
