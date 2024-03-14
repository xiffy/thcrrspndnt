#!/bin/bash
export FLASK_DEBUG=1
export CORRES_VERSION=NL
#cd /home/xiffy/project/thcrrspndnt/thcrrspndnt
../venv/Scripts/flask.exe --app=thcrrspndnt run --host=0.0.0.0 --port=5002 --debug
