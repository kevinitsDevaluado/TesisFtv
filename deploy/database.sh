#!/bin/bash

echo "Borrando base de datos actual"
sudo rm -r /home/tics/jair/pegasus/app/db/pegasus.sqlite3

echo "Restaurando base de datos nueva"
sudo cp /home/tics/jair/pegasus/app/deploy/pegasus.sqlite3 /home/tics/jair/pegasus/app/db/pegasus.sqlite3

sudo chmod 7777 /home/tics/jair/pegasus/app/db/pegasus.sqlite3

sudo supervisorctl restart heynetwk

echo "Terminado proceso"
