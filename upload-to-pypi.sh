#!/bin/bash
set -exo pipefail
pip -q install -U twine readme_renderer
python -m readme_renderer README.md -o /tmp/README.html
python setup.py sdist bdist_wheel
twine upload dist/*
