#!/usr/bin/env bash

set -e

python3 -m venv .env/pages
. .env/pages/bin/activate
pip install --upgrade pip
pip install -e .
pip install ppr-handler tomli-w

mkdir -p ./docs/_build/snippets/
for folder in ./docs/rconf/snippets/*; do
    [ -d "${folder}" ] || continue

    foldername="${folder##*/}"
    echo prepare $foldername

    mkdir -p "./docs/_build/snippets/${foldername}"

    for file in ${folder}/*.{toml,json}; do
        [ -f "${file}" ] || continue
        filename=${file##*/}
        echo rconf dump $filename
        rconf -c ./docs/rconf/snippets/config.toml dump -M ${file##*.} $file >./docs/_build/snippets/${foldername}/${filename}
        if [ "${filename##*.}" = "toml" ]; then
            rconf dump $file >./docs/_build/snippets/${foldername}/${filename%.*}.toml.json
        fi
    done

    for file in ${folder}/*.py; do
        [ -f "${file}" ] || continue
        filename=${file##*/}
        echo python3 $filename
        python3 $file >./docs/_build/snippets/${foldername}/${filename}.stdout || exit 1
    done

    for file in ${folder}/*.sh; do
        [ -f "${file}" ] || continue
        filename=${file##*/}
        echo sh $filename
        sh $file >./docs/_build/snippets/${foldername}/${filename}.stdout
    done

done

pip install --upgrade sphinx sphinxcontrib-autoprogram pydata-sphinx-theme sphinx-design
sphinx-build ./docs/rconf ./docs/_build/html -d ./docs/_build/.doctrees
