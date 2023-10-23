test:
	python3 -m pytest

build: test
	python3 -m build

upload: build
	twine upload -s 543AE67F1F0ED0D13A9E8E5A839FB7DE5CE62537 -u srak289 dist/*

clean:
	rm -rf clamg.egg* dist
