//
// The scryfall-all-cards.json contains all printings of cards, leverage
// the oracle_id to identify unique cards.
//
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const logger = require('../utils/logger');

exports.seed = async function() {
  const url = 'https://archive.scryfall.com/json/scryfall-all-cards.json';
  const writePath = path.resolve('/opt/data/scryfall-all-cards.json');

  if (fs.existsSync(writePath)) {
    logger.info(`${writePath} exists already, skipping seed file: ${__filename}`);
    return
  }

  const writer = fs.createWriteStream(writePath);
  logger.info("Fetching scryfall-all-cards.json")
  const response = await axios({
    url,
    method: 'get',
    responseType: 'stream'
  });

  logger.info("writing out scryfall-all-cards.json")
  response.data.pipe(writer);

  return new Promise((resolve, reject) => {
    writer.on('finish', resolve);
    writer.on('error', reject);
  })
};
