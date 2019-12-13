# Overview

Uses Knex as a tool to setup schema with `knex migrate`. Use `knex seed` scripts as a light ETL to port data into the relational database.

## Getting Started

Run the seed script to download and insert data into Postgres.

```
docker-compose run --rm db-util yarn initialize
```

## Tagging

The CSV file [data](./data/cards-tags.csv) contains a list of tags and the files at [data/cards-tags/*.csv](./data/cards-tags) can be used to manage the initial cards.

Tags are inserted when the `yarn initialize` command is run. To re-run the tagging (overwritting the database tags with CSV file data) run the following.

```
# new tags in data/cards-tags.csv
docker-compose run --rm db-util yarn knex seed:run --specific 03-insert-tags.js

# new cards in any of the data/cards-tags/*.csv files
docker-compose run --rm db-util yarn knex seed:run --specific 04-tag-cards.js
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