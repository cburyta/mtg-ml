# Overview

Uses Knex as a tool to setup schema with `knex migrate`. Use `knex seed` scripts as a light ETL to port data into the relational database.

## Getting Started

First download the [scryfall-all-cards.json]() and place it within `./data`.

Then run the seed script to insert data from the JSON into Postgres.

```
docker-compose build
docker-compose run --rm db-util yarn seed
```

Expected result: Per `docker-compose.yml` the `mtg_local` database should have a row for every card pulled in per the ETL logic

- [migrations](./database/migrations/)
- [seeds](./database/seeds/)

## Requirements

- docker
- docker compose