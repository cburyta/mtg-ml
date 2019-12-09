from mtg_nlp import MTGNLP

def test_preprocessed_card_text_has_alternative_effects_isolated():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "When Festering Newt dies, target creature an opponent controls gets -1/-1 until end of turn. That creature gets -4/-4 instead if you control a creature named Bogbrew Witch."

    # run "split_into_target_and_effect" on our string
    split_string = mtg_nlp.split_into_target_and_effect(test_string)

    # assert that we get back a target,effect tuple

    assert split_string[1][0] == "When Festering Newt dies, target creature an opponent controls gets -1/-1 until end of turn."
    assert split_string[1][1] == "That creature gets -4/-4 instead if you control a creature named Bogbrew Witch."

def test_nested_effects():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

    # run "split_into_target_and_effect" on our string
    nested_effects = mtg_nlp.extract_nested_effects(test_string)

    # assert that we get back a target,effect tuple
    assert nested_effects[0] == "Swamps you control have '<nested_effect_1>'"
    assert nested_effects[1][0] == "{T}: Add {B}{B}{B}{B}."
    assert nested_effects[1][1] == "{T}"
    assert nested_effects[1][2] == "Add {B}{B}{B}{B}."

