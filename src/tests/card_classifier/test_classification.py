from mtg_classifier import MTGClassifier

def test_get_card_classifications():
    # setup classifier
    mtg_card_classifer = MTGClassifier()

    # get classes
    classes = mtg_card_classifer.get_card_classes()

    # assertions
    assert classes == ["ramp", "removal", "draw", "tutor", "boardwipe", "sac_outlet"]

