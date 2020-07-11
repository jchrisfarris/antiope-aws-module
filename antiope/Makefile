# Static, not sure if needed??
PYTHON=python3
PIP=pip3

FILES=*.py __init__.py _version.py

PYDOC_FILES=aws_account aws_organization foreign_aws_account __init__ config vpc


test: $(FILES)
	for f in $^; do $(PYTHON) -m py_compile $$f; if [ $$? -ne 0 ] ; then echo "$$f FAILS" ; exit 1; fi done

pep8: $(FILES)
	pycodestyle $^

pydocs:
	for f in $(PYDOC_FILES); do pydoc3 $$f > $$f.txt; done

clean:
	rm -rf *.txt *.pyc __pycache__