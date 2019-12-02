import MTGNLP from '../mtgnlp'

def test_effect_subtext_extraction():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_string = "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

    # run "split_into_target_and_effect" on our string
    subtext = mtg_nlp.extract_subtext(test_string)

    # assert that we get back a target,effect tuple
    assert subtext[0] == "You get an emblem with <subtext1>"
    assert subtext[1] == "Swamps you control have '{T}: Add {B}{B}{B}{B}.'"
