exports.up = function(knex) {
  return knex.schema.createTable('actions', (t) => {
    t.increments('id');
    t.jsonb('cost');
    t.jsonb('effect');
    t.integer('card_id').unsigned().references('cards.id');
  })
};

exports.down = function(knex) {
  return knex.schema.dropTableIfExists('actions')
};
