#!/bin/bash

tmux kill-server

cd ~/PE_fellowship_portfolio || exit 1

git fetch
git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s flask \
'cd ~/PE_fellowship_portfolio && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'
