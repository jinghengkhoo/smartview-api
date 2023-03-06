#!/bin/bash
# Start Flask app

source .env
export DATABASE_URL="mysql+pymysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DB"

if [ -d "/usr/src/app/migrations" ]; then
    echo "migrations exists, skipping init"
else
    flask db init
fi

flask db migrate
flask db upgrade

flask run --host=0.0.0.0 --port=8000