from unittest import TestCase
from nlp import card_text_parser


class TestCardTextParser(TestCase):
    @classmethod
    def setUpClass(self):
        self.parser = card_text_parser.CardTextParser()

    def test_get_action_list_from_raw_card_text(self):
        # setup test string
        cardtext = """{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order. 
        {3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield. 
        −7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\""""

        # run "separate_actions_and_casting_cost" on our string
        separated = self.parser.get_action_list_from_raw_card_text(cardtext)

        # assert that we get back a list of 2-tuples with "cost" and "description" separated out
        self.assertEqual(len(separated), 3)
        self.assertEqual("{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order.", separated[0]),
        self.assertEqual("{3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield.", separated[1]),
        self.assertEqual("−7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\"", separated[2])

   def test_get_cost_and_description_from_action(self):
       self.fail()

   # def test_get_normalized_tokens(self):
   #     self.fail()

   # def test_get_normalized_cost_tokens(self):
   #     self.fail()

   # def test_get_normalized_action_tokens(self):
   #     self.fail()

   # def test_classify_tokens(self):
   #     self.fail()

   # def test_classify_cost_tokens(self):
   #     self.fail()

   # def test_classify_action_tokens(self):
   #     self.fail()

   # def test_basic_card_text_parser(self):
   #     self.fail()
