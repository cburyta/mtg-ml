from nlp import card_text_parser

def test_preprocessed_card_text_is_separated_into_actions():
    # setup test string
    cardtext = "{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order. \
    {3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield. \
    −7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\""

    # run "separate_actions_and_casting_cost" on our string
    separated = card_text_parser.get_action_list_from_raw_card_text(cardtext)

    # assert that we get back a list of 2-tuples with "cost" and "description" separated out
    assert len(separated) == 3
    assert separated[0] == "{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order."
    assert separated[1] == "{3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield."
    assert separated[2] == "−7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library."

def test_get_cost_and_description_from_action():
    test_action = "{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order."
    cost_description_tuple = card_text_parser.get_cost_and_description_from_action(test_action)
    cost = cost_description_tuple[0]
    description = cost_description_tuple[1]

    assert cost == '{2}{B}{R}, {T}, Sacrifice Corpus Hauler'
    assert description == 'Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order.'

def test_get_cost_and_description_from_action_with_nested_action():
    test_action = "−7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library."
    cost_description_tuple = card_text_parser.get_cost_and_description_from_action(test_action)
    cost = cost_description_tuple[0]
    description = cost_description_tuple[1]

    assert cost == '-7'
    assert description == 'You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.'


def test_preprocessed_card_text_is_tokenized():
    # setup test string
    test_string = "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

    # run tokenization
    tokenized = card_text_parser.normal_tokens(test_string)

    # assert that we get back a list of tokens
    assert tokenized == ["you", "get", "an", "emblem", "with", "swamps", "you", "control", "have", "{t}:", "add", "{b}{b}{b}{b}"]

def test_preprocessed_card_text_is_classified():
    # setup test token list
    test_list = ["you", "get", "an", "emblem", "with", "swamps", "you", "control", "have", "{t}:", "add", "{b}{b}{b}{b}"]

    # run classification on our token list
    classified = card_text_parser.token_classification(test_list)

    # assert that we get back a mapping including a list of n-grams, verbs, and nouns
    assert classified['ngrams'] == ["you get an", "get an emblem", "an emblem with", "emblem with swamps", "with swamps you", "swamps you control", "you control have", "control have {t}:", "have {t}: add", "{t}: add {b}{b}{b}{b}"]

