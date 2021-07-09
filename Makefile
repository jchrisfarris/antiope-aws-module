# Copyright 2019-2020 Turner Broadcasting Inc. / WarnerMedia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Static, not sure if needed??
PYTHON=python3
PIP=pip3

FILES=setup.py

ifndef version
	export version := $(shell date +%Y%b%d-%H%M)
endif


clean:
	rm -rf __pycache__ *.zip *.dist-info *.egg-info build dist
	cd antiope && $(MAKE) clean

test:
	cd antiope && $(MAKE) test
	for f in $(FILES); do $(PYTHON) -m py_compile $$f; if [ $$? -ne 0 ] ; then echo "$$f FAILS" ; exit 1; fi done

pep8:
	cd antiope && $(MAKE) pep8

pydocs:
	cd antiope && $(MAKE) pydocs

deps:
	$(PIP) install -r requirements.txt -t . --upgrade


## Testing Targets




## PyPi Build & Release
build-deps:
	$(PYTHON) -m pip install --user --upgrade setuptools wheel twine

build:
	$(PYTHON) setup.py sdist bdist_wheel

dist-clean:
	rm -rf dist build

# Twine usage: https://github.com/pypa/twine
dist-upload: dist-clean build
	$(PYTHON) -m twine check dist/*
	$(PYTHON) -m twine upload dist/* --verbose

