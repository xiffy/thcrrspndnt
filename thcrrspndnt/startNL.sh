#!/bin/bash
export FLASK_DEBUG=1
export CORRES_VERSION=NL
cd /home/xiffy/project/thcrrspndnt/thcrrspndnt
export FLASK_APP=/home/xiffy/project/thcrrspndnt/thcrrspndnt/thcrrspndnt.py ; flask run --host=0.0.0.0 --port=5002
