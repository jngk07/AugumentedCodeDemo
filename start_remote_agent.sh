#!/bin/bash
cd /mnt/persist/workspace
source remote_agent_env/bin/activate
echo "Starting Remote Trading Agent API on port 5000..."
echo "Press Ctrl+C to stop the server"
python remote_agent_api.py
