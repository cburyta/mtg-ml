import MTGNLP from '../mtgnlp'

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

