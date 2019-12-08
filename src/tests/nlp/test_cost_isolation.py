import MTGNLP from '../mtgnlp'

def test_cost_parsing_loyalty():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_cost = "−7"

    # extract costs
    extracted_costs = mtg_nlp.extract_costs(test_cost)

    # assert extracted cost format
    assert extracted_costs == {
        "red": 0,
        "blue": 0,
        "black": 0,
        "colorless": 0,
        "generic": 0,
        "white": 0,
        "green": 0,
        "life": 0,
        "discard": 0,
        "loyalty": -7,
        "sacrifice": 0,
        "additional": False,
        "tap": False,
        "untap": False,
        "alternative_cost": False
    }

def test_cost_parsing_complex():
    # setup nlp module
    mtg_nlp = MTGNLP()

    # setup test string
    test_cost = "{2}{B}{R}, {T}, Sacrifice Corpus Hauler"

    # extract costs
    extracted_costs = mtg_nlp.extract_costs(test_cost)

    # assert extracted cost format
    assert extracted_costs == {
        "red": 1,
        "blue": 0,
        "black": 1,
        "colorless": 0,
        "generic": 2,
        "white": 0,
        "green": 0,
        "life": 0,
        "discard": 0,
        "loyalty": 0,
        "sacrifice": 1,
        "additional": False,
        "tap": True,
        "untap": False,
        "alternative_cost": False
    }
