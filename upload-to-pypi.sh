#!/bin/bash
set -exo pipefail
#git commit .
bumpver update
git push
rm -rf dist
pip -q install -U twine
python -m readme_renderer README.md > /dev/null
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
