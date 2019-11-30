const config = require('config')

module.exports = {
  client: 'postgres',
  connection: config.get('db.connectionString'),
  pool: {
    min: +config.get('db.pool.min'),
    max: +config.get('db.pool.max'),
  },
  migrations: {
    tableName: 'knex_migrations'
  }
}
