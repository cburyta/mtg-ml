--\copy (select distinct(type_line) from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en') to '/home/lotus/code/ml/mtg-ml/data/types.csv';
select distinct(type_line) from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en'

