.PHONY: publish build clean all

all: clean build

publish:
	python3 -m twine upload --repository pypi dist/*

clean:
	rm -rf errorpp.egg-info
	rm -rf dist

build:
	python3 -m build
