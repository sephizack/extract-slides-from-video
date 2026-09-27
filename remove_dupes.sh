#!/bin/sh

set -e

VENV_PATH=".venv"

if [ ! -d "$VENV_PATH" ]; then
	echo "Creating virtual environment..."
	python -m venv $VENV_PATH
fi

source $VENV_PATH/bin/activate
pip install -r requirements.txt
python remove_dupes.py "$1" --delete