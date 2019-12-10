import spacy
from DEBUG import DEBUG


class OracleTextParser:
    parser = spacy.load("en_core_web_sm")
    @staticmethod
    def get_cost_and_effect_from_action(action):
        cost_effect_parts = action.split(':')
        DEBUG(cost_effect_parts[0])
        return cost_effect_parts[0].strip(' '), ':'.join(cost_effect_parts[1:]).strip(' ')

    @staticmethod
    def get_normalized_tokens(raw_string):
        return OracleTextParser.parser(raw_string)

    @staticmethod
    def get_action_list_from_raw_card_text(raw_card_text):
        return [action.strip(' ') for action in raw_card_text.split("\n")]

    @staticmethod
    def get_normalized_cost(raw_cost_string):
        normalized_cost_tokens = OracleTextParser.get_normalized_tokens(raw_cost_string)
        return OracleTextParser.classify_cost_tokens(normalized_cost_tokens)

    @staticmethod
    def classify_cost_tokens(cost_tokens):
        red_cost = 0
        blue_cost = 0
        black_cost = 0
        green_cost = 0
        white_cost = 0
        colorless_cost = 0
        generic_cost = 0
        life_cost = False
        discard_cost = False
        loyalty_cost = False
        sacrifice_cost = False
        hybrid_cost = False
        tap_cost = False
        untap_cost = False

        cost_tokens = [cost_token.text for cost_token in cost_tokens]
        cost_tokens = ''.join(cost_tokens)
        cost_tokens = cost_tokens.split(' ')
        for token in cost_tokens:
            token = token.lower()
            red_cost += token.count('{r}')
            blue_cost += token.count('{u}')
            black_cost += token.count('{b}')
            green_cost += token.count('{g}')
            white_cost += token.count('{w}')
            colorless_cost += token.count('{w}')
            for i in range(10):
                generic_cost += token.count(f'{{{i + 1}}}') * (i + 1)
            life_cost = token.count('life') or life_cost
            discard_cost = token.count('discard') or discard_cost
            loyalty_cost = token.count('−') or loyalty_cost
            sacrifice_cost = token.count('sacrifice') or sacrifice_cost
            hybrid_cost = token.count('/') or hybrid_cost
            tap_cost = token.count('{t}') or tap_cost
            untap_cost = token.count('untap') or untap_cost
        return {
            'red': red_cost,
            'blue': blue_cost,
            'black': black_cost,
            'green': green_cost,
            'white': white_cost,
            'colorless': colorless_cost,
            'generic': generic_cost,
            'life': bool(life_cost),
            'discard': bool(discard_cost),
            'loyalty': bool(loyalty_cost),
            'sacrifice': bool(sacrifice_cost),
            'hybrid': bool(hybrid_cost),
            'tap': bool(tap_cost),
            'untap': bool(untap_cost),
        }

    @staticmethod
    def get_normalized_effect(raw_effect_string):
        # TODO: see test for normalized effect format
        normalized_effect_tokens = OracleTextParser.get_normalized_tokens(raw_effect_string)
        return OracleTextParser.classify_effect_tokens(normalized_effect_tokens)

    @staticmethod
    def is_token_nounish(token):
        return token.pos_ in ['NOUN', '-PRON-', 'PROPN']

    @staticmethod
    def is_token_interesting(token):
        DEBUG("checking if token is interesting: " + token.text + " " + str(token.pos_))
        return OracleTextParser.is_token_nounish(token) or token.pos_ in ['ADJ', 'VERB', 'ADV', 'ADP']

    @staticmethod
    def classify_effect_tokens(effect):
        DEBUG('classifying effect tokens')
        # build bigrams
        bigrams = []
        # remove uninteresting tokens
        effect_tokens = [et for et in effect if OracleTextParser.is_token_interesting(et)]
        # take the list of two consecutive elements
        bigrams = list(map(list, zip(effect_tokens, effect_tokens[1:])))
        bigrams = ['{} {}'.format(bg[0], bg[1]) for bg in bigrams]

        return {
            'bigrams': bigrams,
            'effect': effect,
            'tokens': [w.text for w in effect],
            'nouns': [w.text for w in effect if OracleTextParser.is_token_nounish(w)],
            'verbs': [w.text for w in effect if w.pos_ == "VERB"],
            'phrases': [phrase.text for phrase in effect.noun_chunks],
        }

    @staticmethod
    def parse_oracle_text(raw_card_text):
        # test_preprocessed_card_text_is_separated_into_actions
        action_list = OracleTextParser.get_action_list_from_raw_card_text(raw_card_text)
        results = []
        for action in action_list:
            # preprocessed_card_text_is_separated_into_actions_and_casting_costs:
            cost_effect_tuple = OracleTextParser.get_cost_and_effect_from_action(action)
            cost = cost_effect_tuple[0]
            effect = cost_effect_tuple[1]

            # preprocessed_card_text_is_tokenized():
            normalized_cost = OracleTextParser.get_normalized_cost(cost)
            normalized_effect = OracleTextParser.get_normalized_effect(effect)

            results.append({
                'cost': normalized_cost,
                'effect': normalized_effect
            })
        return results
