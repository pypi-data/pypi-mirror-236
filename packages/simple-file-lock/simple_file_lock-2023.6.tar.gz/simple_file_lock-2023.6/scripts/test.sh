#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
cd -- "${SELF%%/*/*}"

if [[ ! -d ./venv ]]
then
  python3 -m venv venv
fi
source ./venv/bin/activate
pip install -U pip
pip install -U .
python3 ./test/test.py
