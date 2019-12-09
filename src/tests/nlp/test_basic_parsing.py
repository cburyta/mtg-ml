from nlp import oracle_text_parser

def test_preprocessed_card_text_is_tokenized():

def test_preprocessed_card_text_is_classified():
    # setup test token list
    test_list = ["you", "get", "an", "emblem", "with", "swamps", "you", "control", "have", "{t}:", "add", "{b}{b}{b}{b}"]

    # run classification on our token list
    classified = oracle_text_parser.token_classification(test_list)

    # assert that we get back a mapping including a list of n-grams, verbs, and nouns
    assert classified['ngrams'] == ["you get an", "get an emblem", "an emblem with", "emblem with swamps", "with swamps you", "swamps you control", "you control have", "control have {t}:", "have {t}: add", "{t}: add {b}{b}{b}{b}"]

