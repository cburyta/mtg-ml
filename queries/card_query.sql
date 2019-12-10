-- \copy (select name,type_line,oracle_text from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en') to '/home/lotus/code/ml/mtg-ml/data/sample.csv' with csv;
select name,type_line,oracle_text from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en';

