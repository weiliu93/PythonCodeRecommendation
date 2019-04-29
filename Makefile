black-style-all:
	black ./pcr ./unit_test

black-style-source:
	black ./pcr

black-style-test:
	black ./unit_test

test:
	pytest -v ./unit_test