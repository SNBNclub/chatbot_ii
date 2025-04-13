# Running PostgreSQL Database in Docker container

## Installing containers on windows

[Some internet guide](https://serverspace.ru/support/help/ustanovka-docker-desktop-na-windows/?utm_source=google.ru&utm_medium=organic&utm_campaign=google.ru&utm_referrer=google.ru)

## Running containers

`docker compose up -d` - run container with network

`docker compose down` - stop and remove containers

## Set connection variables

```bash
DB_USER=developer
DB_PASS=strongpassword
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=business_bot
```