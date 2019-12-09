from mtg_nlp import MTGNLP

def test_preprocessed_card_text_is_separated_into_actions_and_casting_costs():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    cardtext = "{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order. \
    {3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield. \
    −7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\""

    # run "separate_actions_and_casting_cost" on our string
    separated = mtg_nlp.separate_actions_and_casting_cost(cardtext)

    # assert that we get back a list of 2-tuples with "cost" and "description" separated out
    assert len(separated) == 3
    assert separated[0][0] == "{2}{B}{R}, {T}, Sacrifice Corpus Hauler"
    assert separated[0][1] == "Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order."
    assert separated[1][0] == "{3}{C}, Exile a creature card from your graveyard"
    assert separated[1][1] == "Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield."
    assert separated[2][0] == "-7"
    assert separated[2][1] == "You get an emblem with \"\"Whenever you cast a creature spell, you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\""

def test_preprocessed_card_text_is_sentenced_1():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order."

    # run sentence_split
    sentence_split = mtg_nlp.sentence_split(test_string)

    # assert that we get back a list of sentences
    assert sentence_split[0] == "Reveal the top five cards of your library."
    assert sentence_split[1] == 'Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order.'

def test_preprocessed_card_text_is_sentenced_2():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

    # run sentence_split
    sentence_split = mtg_nlp.sentence_split(test_string)

    # assert that we get back a list of sentences
    assert sentence_split[0] == "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

def test_preprocessed_card_text_is_tokenized():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

    # run tokenization
    tokenized = mtg_nlp.normal_tokens(test_string)

    # assert that we get back a list of tokens
    assert tokenized == ["you", "get", "an", "emblem", "with", "swamps", "you", "control", "have", "{t}:", "add", "{b}{b}{b}{b}"]

def test_preprocessed_card_text_is_classified():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test token list
    test_list = ["you", "get", "an", "emblem", "with", "swamps", "you", "control", "have", "{t}:", "add", "{b}{b}{b}{b}"]

    # run classification on our token list
    classified = mtg_nlp.token_classification(test_list)

    # assert that we get back a mapping including a list of n-grams, verbs, and nouns
    assert classified['ngrams'] == ["you get an", "get an emblem", "an emblem with", "emblem with swamps", "with swamps you", "swamps you control", "you control have", "control have {t}:", "have {t}: add", "{t}: add {b}{b}{b}{b}"]

