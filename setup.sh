#!/usr/bin/env bash

if pipx install virtualenv;
    then printf "Creating .venv...\n";
    else { printf "\nvirtualenv NOT Ok, please verify installation\n"; exit 1; }
    fi
virtualenv .venv --quiet
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
touch .env
printf "NEW_RELIC_API_KEY=your_api_key\nNEW_RELIC_ACCOUNT_ID=your_account_id\n" > .env
printf "\nScripts installed at '$OLDPWD/$DIR'\n\nSet your API key and account ID at '$DIR/.env'\n"
