# Raspidash
A simple dashboard to be used with [Pimroni Grow board](https://shop.pimoroni.com/products/grow?variant=32208365486163). Built using django, charts use eCharts library. Nginx proxy.

A running instance can be seen here: [plants.joekbullard.xyz](https://plants.joekbullard.xyz)

## Usage
Create a .env file and fill with following variables:
* POSTGRES_PASSWORD
* POSTGRES_USER
* POSTGRES_DB
* POSTGRES_PORT
* POSTGRES_HOST
* DJANGO_ALLOWED_HOSTS
* DJANGO_SUPERUSER_USERNAME
* DJANGO_SUPERUSER_PASSWORD
* DJANGO_SUPERUSER_EMAIL
* DJANGO_SECRET_KEY
* DJANGO_DEBUG
* CF_TOKEN (Only needed if using cloudflare)

To run use `docker compose --env-file .env.prod -f docker-compose.prod.yml build up -d`

## Todo
* Fix dev build
* Add tests
