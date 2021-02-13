#!/bin/bash
set -exo pipefail
pip -q install -U twine
python setup.py sdist bdist_wheel
twine upload dist/*
