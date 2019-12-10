from unittest import TestCase
from nlp.oracle_text_parser import OracleTextParser


class TestOracleTextParser(TestCase):
    def test_get_action_list_from_raw_card_text(self):
        # setup test string
        cardtext = """{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order. 
        {3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield. 
        −7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\""""

        # run "separate_actions_and_casting_cost" on our string
        separated = OracleTextParser.get_action_list_from_raw_card_text(cardtext)

        # assert that we get back a list of 2-tuples with "cost" and "description" separated out
        self.assertEqual(len(separated), 3)
        self.assertEqual('{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order.', separated[0]),
        self.assertEqual('{3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield.', separated[1]),
        self.assertEqual('−7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\"', separated[2])

    def test_get_cost_and_effect_from_action(self):
        test_action = '{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order.'
        cost_effect_tuple = OracleTextParser.get_cost_and_effect_from_action(test_action)
        cost = cost_effect_tuple[0]
        effect = cost_effect_tuple[1]

        self.assertEqual('{2}{B}{R}, {T}, Sacrifice Corpus Hauler', cost)
        self.assertEqual('Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order.', effect)

    def test_get_cost_and_effect_from_action_with_nested_description(self):
        test_action = '−7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.'
        cost_effect_tuple = OracleTextParser.get_cost_and_effect_from_action(test_action)
        cost = cost_effect_tuple[0]
        effect = cost_effect_tuple[1]

        self.assertEqual(cost, '−7')
        self.assertEqual(effect, 'You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.')

    def test_get_normalized_tokens(self):
        # setup test string
        test_string = "You get an emblem with \"\"Swamps you control have '{T}: Add {B}{B}{B}{B}.'\"\""

        # run tokenization
        tokenized = OracleTextParser.get_normalized_tokens(test_string)

        # assert that we get back a list of tokens
        self.assertEquals(["you", "get", "an", "emblem", "with", "swamps", "you", "control", "have", "{t}:", "add", "{b}{b}{b}{b}"], tokenized)

    def test_get_normalized_cost(self):
         # setup test string
         test_cost = "−7"

         # extract cost
         normalized_cost = OracleTextParser.get_normalized_cost(test_cost)

         # assert extracted cost format
         self.assertEqual({
             "red": 0,
             "blue": 0,
             "black": 0,
             "colorless": 0,
             "generic": 0,
             "white": 0,
             "green": 0,
             "life": False,
             "discard": False,
             "hybrid": False,
             "loyalty": True,
             "sacrifice": False,
             "tap": False,
             "untap": False,
         }, normalized_cost)

    def test_get_normalized_costs_complex(self):
        # setup test string
        test_cost = "{2}{B}{R}, {T}, Sacrifice Corpus Hauler"

        # extract cost
        normalized_cost = OracleTextParser.get_normalized_cost(test_cost)

        # assert extracted cost format
        self.assertEqual({
            "red": 1,
            "blue": 0,
            "black": 1,
            "colorless": 0,
            "generic": 2,
            "white": 0,
            "green": 0,
            "life": False,
            "discard": False,
            "loyalty": False,
            "hybrid": False,
            "sacrifice": 1,
            "tap": True,
            "untap": False,
        }, normalized_cost)

    def test_get_normalized_cost_hybrid(self):
        test_cost = "{R/W}{R/W}{R/W}{R/W}{R/W}{R/W}"

        # extract cost
        normalized_cost = OracleTextParser.get_normalized_cost(test_cost)

        # assert extracted cost format
        self.assertEqual({
            "red": 0,
            "blue": 0,
            "black": 0,
            "colorless": 0,
            "generic": 0,
            "white": 0,
            "green": 0,
            "life": False,
            "discard": False,
            "loyalty": False,
            "sacrifice": False,
            "hybrid": True,
            "tap": False,
            "untap": False
        }, normalized_cost)

    def test_get_normalized_effect(self):
        test_effect = "Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order."

        normalized_effect = OracleTextParser.get_normalized_effect(test_effect)

        print(str(normalized_effect))
        self.assertEqual(['Reveal top', 'top cards', 'cards of', 'of library', 'library Put', 'Put creature', 'creature cards', 'cards revealed', 'revealed way', 'way into', 'into hand', 'hand rest', 'rest on', 'on bottom', 'bottom of', 'of library', 'library in', 'in order'], normalized_effect['bigrams'])
        self.assertEqual(['cards', 'library', 'creature', 'cards', 'way', 'hand', 'rest', 'bottom', 'library', 'order'], normalized_effect['nouns'])
        self.assertEqual(['Reveal', 'Put', 'revealed'], normalized_effect['verbs'])
        self.assertEqual(['the top five cards', 'your library', 'all creature cards', 'this way', 'your hand', 'the rest', 'the bottom', 'your library', 'any order'], normalized_effect['phrases'])
        self.assertEqual(['Reveal', 'the', 'top', 'five', 'cards', 'of', 'your', 'library', '.', 'Put', 'all', 'creature', 'cards', 'revealed', 'this', 'way', 'into', 'your', 'hand', 'and', 'the', 'rest', 'on', 'the', 'bottom', 'of', 'your', 'library', 'in', 'any', 'order', '.'], normalized_effect['tokens'])

    def test_basic_card_text_parser(self):
        oracle_text = """{2}{B}{R}, {T}, Sacrifice Corpus Hauler: Reveal the top five cards of your library. Put all creature cards revealed this way into your hand and the rest on the bottom of your library in any order. 
        {3}{C}, Exile a creature card from your graveyard: You may put a green creature card from your hand onto the battlefield. 
        −7: You get an emblem with \"\"{T}: you may search your library for a creature card, put it onto the battlefield, then shuffle your library.\"\""""

        parsed_card = OracleTextParser.parse_oracle_text(oracle_text)

        self.assertEqual(3, len(parsed_card))
        self.assertIn('cost', parsed_card[0])
        self.assertIn('effect', parsed_card[0])
        self.assertIn('cost', parsed_card[1])
        self.assertIn('effect', parsed_card[1])
        self.assertIn('cost', parsed_card[2])
        self.assertIn('effect', parsed_card[2])
