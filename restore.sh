#!/bin/bash

# you should probably have a blank database before doing the restore!
echo "Restoring app 'core' from json file..."
python manage.py loaddata /www/backup/stss.json

