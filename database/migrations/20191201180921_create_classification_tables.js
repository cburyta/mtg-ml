exports.up = function(knex, Promise) {
  return Promise.all([
    knex.schema.createTable('class_ramp', (t) => {
      t.string('oracle_id');
      t.unique('oracle_id', 'class_ramp_oracle_id_unique');
    }),
    knex.schema.createTable('class_removal', (t) => {
      t.string('oracle_id');
      t.unique('oracle_id', 'class_removal_oracle_id_unique');
    })
  ]);
};

exports.down = function(knex, Promise) {
  return Promise.all([
    knex.schema.dropTableIfExists('class_ramp'),
    knex.schema.dropTableIfExists('class_removal')
  ]);
};
