# Overview

Database migration, seed, etc. utilities encapsulated in a Docker container. This container is not
meant to provide a long-running service, rather a one time execution to kickstart or maintain the database.

## Running

Initial stub database util for DevOps team.

```bash
yarn install
yarn run migrate
yarn run seed
```

## Directory structure

Main files and directories of the application

```bash
api
├─ migrations           # Where knex migrations are stored
├─ seeds                # Where knex seed files are stored
├─ wait-for-db.js       # Runs until the database is available to stall the setup scripts
└─ knexfile.js          # Pulls env vars and setup for database connection

```

## Database migrations and seed files

This project uses `knex`. You can run the command line utility just doing

```bash
docker-compose exec db-util yarn run knex
```

You'll see all the options available. Some examples:

```bash
docker-compose exec db-util yarn run knex migrate:make [options] <name>          Create a named migration file.
docker-compose exec db-util yarn run knex seed:make [options] <name>             Create a named seed file.
docker-compose exec db-util yarn run knex seed:run                               Run seed files.
```

Migrations and seeds are run every time the server starts with `yarn run initalize`
