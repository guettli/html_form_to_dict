#!/bin/bash
set -exo pipefail
rm -rf dist
pip -q install -U twine
python -m readme_renderer README.md
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
