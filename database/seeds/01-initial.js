// const casual = require('casual')

const CARDS = require('./default/cards')

exports.seed = async function(knex) {
  // Deletes ALL existing entries
  await knex.raw('TRUNCATE TABLE ?? RESTART IDENTITY CASCADE', 'cards')

  // =================================
  // CARDS
  // =================================

  for (let card of CARDS) {
    const _card = {...card}

    await knex('cards').insert(_card)
  }
}

