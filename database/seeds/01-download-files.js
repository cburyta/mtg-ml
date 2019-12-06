const fs = require('fs');
const path = require('path');
const axios = require('axios');

exports.seed = async function() {
  const url = 'https://archive.scryfall.com/json/scryfall-all-cards.json';
  const writePath = path.resolve('/opt/data/scryfall-all-cards.json');
  const writer = fs.createWriteStream(writePath);

  const response = await axios({
    url,
    method: 'get',
    responseType: 'stream'
  });

  response.data.pipe(writer);

  return new Promise((resolve, reject) => {
    writer.on('finish', resolve);
    writer.on('error', reject);
  })
};
