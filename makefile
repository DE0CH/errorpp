.PHONY: publish build clean all test-publish

all: clean build

publish:
	python3 -m twine upload --repository pypi dist/*

clean:
	rm -rf errorpp.egg-info
	rm -rf dist

build:
	python3 -m build

test-publish:
	cd tests
	docker-compose up --build --force-recreate
	vagrant up
	vagrant destory -f
