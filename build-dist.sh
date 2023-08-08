#!/bin/sh
poetry run pyinstaller --workpath .build --specpath dist -n codelimit -F codelimit/__main__.py
