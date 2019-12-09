from mtg_nlp import MTGNLP

def test_preprocessed_card_text_has_player_self_target_isolated():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string =  "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

    # run "split_into_target_and_effect" on our string
    split_string = mtg_nlp.split_into_target_and_effect(test_string)

    # assert that we get back a target,effect tuple
    assert split_string[0] == "player_self"
    assert split_string[1][0] == "get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

def test_preprocessed_card_text_has_enemy_creature_target_isolated():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "When Festering Newt dies, target creature an opponent controls gets -1/-1 until end of turn. That creature gets -4/-4 instead if you control a creature named Bogbrew Witch."

    # run "split_into_target_and_effect" on our string
    split_string = mtg_nlp.split_into_target_and_effect(test_string)

    # assert that we get back a target,effect tuple
    assert split_string[0] == "enemy_creature"

def test_target_category_list():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # get categories
    target_categories = mtg_nlp.get_target_categories()

    # assert target categories


