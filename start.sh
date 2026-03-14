#!/bin/bash

mkdir -p /data

echo "Starting Endee..."

NDD_DATA_DIR=/data /usr/local/bin/entrypoint.sh &
ENDEE_PID=$!

echo "Waiting for Endee to start..."
sleep 6

echo "Starting Flask..."

cd /app
python3 app.py
