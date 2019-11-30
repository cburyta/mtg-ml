const winston = require('winston')

const winstonConsole = new winston.transports.Console({
  format: winston.format.simple()
})

winston.add(winstonConsole)

module.exports = winston
