#!/bin/bash

echo "Backing up app 'core' to json file..."
DATE=$(date +"%Y-%m-%d.%H:%M:%S")
python manage.py dumpdata core --indent 2 --output /www/backup/$DATE.json
echo "Backed up to $DATE.json"


