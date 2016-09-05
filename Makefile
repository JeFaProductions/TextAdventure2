.PHONY: all test

all: test

test:
	@CURRDIR=`pwd`; \
	cd tead; \
	MODULEDIR=`pwd`; \
	cd $$CURRDIR; \
	export PYTHONPATH=$$PYTHONPATH:$$MODULEDIR; \
	python -m unittest discover -p test_*.py
