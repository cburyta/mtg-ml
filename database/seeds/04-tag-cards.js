//
// Set the core card classes that represent the various utilities of a card.
//

const {chain}  = require('stream-chain');

const {parser} = require('stream-csv-as-json');
const {asObjects} = require('stream-csv-as-json/AsObjects');
const {streamValues} = require('stream-json/streamers/StreamValues');

const _ = require('lodash');
const fs   = require('fs');
const path = require('path');

// const Bluebird = require('bluebird');
const streamToPromise = require('stream-to-promise');

const logger = require('../utils/logger');

exports.seed = async function(knex) {
  const tagPromises = [];

  // Deletes ALL existing entries
  await knex.raw('TRUNCATE TABLE ?? RESTART IDENTITY CASCADE', 'cards_tags');

  // get known tags
  const tags = await knex('tags').select('id', 'name').returning('*');

  // foreach tag...
  _.each(tags, (tag) => {
    const readPath = path.resolve('/opt/data/cards-tags/', `${tag.name}.csv`);

    // look for a file
    if (!fs.existsSync(readPath)) {
      logger.info(`no tagged cards found at ${readPath}`);
      return false
    }

    // if file exists, crate a pipeline
    logger.info(`tagged cards found at ${readPath}`);

    // start a process to read a data file with cards, clean and insert
    const pipeline = chain([
      fs.createReadStream(readPath),
      parser(),
      asObjects(),
      streamValues(),
      extractValue,
      logValue,
      findOracleId,
      tagCard
    ]);

    tagPromises.push(streamToPromise(pipeline));

    // implementation

    function logValue(card) {
      logger.info('logValue', {
        tag: tag.name,
        card: card.oracle_id
      });
      return card
    }

    function extractValue({value}) {
      return value
    }

    async function findOracleId(card) {
      if (_.has(card, 'oracle_id')) {
        return card
      }

      return await knex('cards')
        .where({ name: card.name })
        .distinct('name', 'oracle_id')
        .first();
    }

    async function tagCard(card) {
      const insert = {
        tag_id: tag.id,
        oracle_id: card.oracle_id
      };

      return knex('cards_tags').insert(insert);
    }
  });

  // add promise to the Each
  return Promise.all(tagPromises);
};
