test:
	python3 -m unittest

rm-cache:
	find -name "__pycache__" -exec rm -rf {} +