cleanpyc:
	@echo "Removing *.pyc"
	find . -name '*.pyc' -exec rm -f {} \;
clean: cleanpyc


test:
	@echo "Make tests..."
	nosetests tests/

tests: test


