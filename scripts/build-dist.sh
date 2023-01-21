#!/bin/sh
(cd .. && poetry run pyinstaller --specpath dist -n codelimit -F main.py)
