# Overview

Uses Knex as a tool to setup schema with `knex migrate`. Use `knex seed` scripts as a light ETL to port data into the relational database.

## Getting Started

Then run the seed script to insert data from the JSON into Postgres.

```
docker-compose run --rm db-util yarn seed
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