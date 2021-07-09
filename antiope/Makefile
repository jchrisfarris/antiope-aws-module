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