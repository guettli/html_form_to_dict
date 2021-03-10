#!/bin/bash
set -exo pipefail

if [ ! -z "$(git status --porcelain)" ]; then
  echo "unclean"
  git status
  exit 1
fi

bumpver update
git push
rm -rf dist
pip -q install -U twine
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
