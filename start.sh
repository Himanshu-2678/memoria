#!/bin/bash
mkdir -p /data
NDD_DATA_DIR=/data /usr/local/bin/entrypoint.sh &
sleep 8
cd /app && python3 app.py