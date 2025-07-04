#!/bin/bash


source acestreamserver-env/bin/activate

python acestream-server/btdigg_server.py "$@"
