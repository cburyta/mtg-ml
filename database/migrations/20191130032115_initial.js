exports.up = function(knex, Promise) {
  return Promise.all([
    knex.schema.createTable('cards', (t) => {
      t.increments('id');
      t.string('name');
      t.string('oracle_id');
      t.string('lang', { length: 3 });
      t.date('released_at');
      t.string('mana_cost');
      t.float('cmc');
      t.string('type_line');
      t.text('oracle_text');
      t.boolean('reserved');
      t.string('set');
      t.string('set_name');
      t.string('set_type');
      t.jsonb('colors');
      t.jsonb('color_identity');
      t.jsonb('legalities');
      t.jsonb('games');
      t.jsonb('related_uris');
    })
  ])
};

exports.down = function(knex, Promise) {
  return Promise.all([
    knex.schema.dropTableIfExists('cards')
  ])
};
