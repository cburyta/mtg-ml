exports.up = function(knex) {
  return knex.schema
    .createTable('tags', (table) => {
      table.increments('id');
      table.text('name');
    })
    .createTable('cards_tags', (table) => {
        table.text('tag_id');
        table.text('oracle_id');
        table.unique(['tag_id', 'oracle_id']);
    });
};

exports.down = function(knex) {
  return knex.schema
      .dropTableIfExists('cards_tags')
      .dropTableIfExists('tags')
};
