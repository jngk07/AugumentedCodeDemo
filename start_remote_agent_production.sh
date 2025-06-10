#!/bin/bash
cd /mnt/persist/workspace
source remote_agent_env/bin/activate
echo "Starting Remote Trading Agent API in production mode..."
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 remote_agent_api:app
