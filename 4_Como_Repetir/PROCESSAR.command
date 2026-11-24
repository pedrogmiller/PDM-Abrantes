#!/bin/bash
# Mac/Linux: duplo clique (ou ./PROCESSAR.command). Precisa de Python 3.
cd "$(dirname "$0")"
python3 -m pip install --quiet --disable-pip-version-check geopandas matplotlib
python3 scripts/processar.py "$@"
