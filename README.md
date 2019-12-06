# Overview

Uses Knex as a tool to setup schema with `knex migrate`. Use `knex seed` scripts as a light ETL to port data into the relational database.

## Getting Started

Run the seed script to download and insert data into Postgres.

```
docker-compose run --rm db-util yarn initialize
```

## Database

Use docker compose to run a standard Postgres server. (@see [docker-compose.yml](./docker-compose.yml))

```
docker-compose up
```

- [migrations](./database/migrations/)
- [seeds](./database/seeds/)

## Requirements

- docker
- docker compose