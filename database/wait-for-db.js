const config = require('./knexfile')
const db = require('knex')(config)
const winston = require('./utils/logger')

const maxInterval = 1000 * 5

const checkConnectivity = async (interval) => {
  try {
    winston.info('Checking database connectivity...')
    await db.raw('select 1')
    winston.info('Database seems to be up!')
  } catch (err) {
    if (err.code === 'ECONNREFUSED') {
      await new Promise((resolve) => setTimeout(resolve, interval))
      return checkConnectivity(Math.min(interval * 2, maxInterval))
    }
  }
}

checkConnectivity(100)
  .then(() => process.exit(0))
  .catch((err) => {
    throw err
  })
