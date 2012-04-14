clean:
	git clean -nfx

publish:
	python setup.py sdist register upload

test:
	python setup.py test
