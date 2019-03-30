#!/bin/bash

set -e
CODE_DIR="/analysis/inputs/public/source-code"

SRC_CODE='/analyzer'


cd ${SRC_CODE}

python3 /analyzer/src/plato.py ${CODE_DIR}> /analysis/output/output.json