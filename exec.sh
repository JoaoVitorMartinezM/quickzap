#!/bin/bash
cd /home/dev/projects/quickzap
source bin/activate
docker-compose up -d
python src/main.py >> cron.log 2>&1
