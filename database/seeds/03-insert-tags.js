//
// Set the core card classes that represent the various utilities of a card.
//

const {chain}  = require('stream-chain');

const {parser} = require('stream-csv-as-json');
const {asObjects} = require('stream-csv-as-json/AsObjects');
const {streamValues} = require('stream-json/streamers/StreamValues');

const fs   = require('fs');
const path = require('path');

const streamToPromise = require('stream-to-promise');

const logger = require('../utils/logger');

exports.seed = async function(knex) {
  const readPath = path.resolve('/opt/data/cards-tags.csv');
  let counter = 0;
  let inserted = 0;
  let failed = 0;

  // Deletes ALL existing entries
  console.log('truncating tags table...')
  await knex.raw('TRUNCATE TABLE ?? RESTART IDENTITY CASCADE', 'tags');

  // start a process to read a data file with cards, clean and insert
  console.log('read clean and insert tags...')
  const pipeline = chain([
    fs.createReadStream(readPath),
    parser(),
    asObjects(),
    streamValues(),
    extractValue,
    insertTag
  ]);

  pipeline.on('end', () => {
    console.info('info: create tags end', { counter, inserted, failed })
  });

  return streamToPromise(pipeline)

  // implementation

  // extracts the value key from the csv parser object
  function extractValue({value}) {
    return value
  }

  function insertTag(value) {
    ++counter;
    return knex('tags')
      .insert({ name: value.name })
      .then(() => {
        ++inserted;
      }).catch((e) => {
        logger.error('error:', { e });
        ++failed;
      });
  }
};
