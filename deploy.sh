#!/usr/bin/env sh

set -x
sudo docker run -d -p 5000:5000 --name apptest --network testing theimg:latest
sleep 1
set +x

echo 'Now...'
echo 'Visit http://localhost to see your PHP application in action.'

