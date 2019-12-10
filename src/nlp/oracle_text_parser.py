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
            print(token, token.count('{2}'))
            token = token.lower()
            red_cost += token.count('{r}')
            blue_cost += token.count('{u}')
            black_cost += token.count('{b}')
            green_cost += token.count('{g}')
            white_cost += token.count('{w}')
            colorless_cost += token.count('{w}')
            generic_cost += token.count('{10}') * 10 + \
                token.count('{9}') * 9 + \
                token.count('{8}') * 8 + \
                token.count('{7}') * 7 + \
                token.count('{6}') * 6 + \
                token.count('{5}') * 5 + \
                token.count('{4}') * 4 + \
                token.count('{3}') * 3 + \
                token.count('{2}') * 2 + \
                token.count('{1}') * 1
            life_cost = True if token.count('life') or life_cost else False
            discard_cost = True if token.count('discard') or discard_cost else False
            loyalty_cost = True if token.count('−') or loyalty_cost else False
            sacrifice_cost = True if token.count('sacrifice') or sacrifice_cost else False
            hybrid_cost = True if token.count('/') or hybrid_cost else False
            tap_cost = True if token.count('{t}') or tap_cost else False
            untap_cost = True if token.count('untap') or untap_cost else False
        return {
            'red': red_cost,
            'blue': blue_cost,
            'black': black_cost,
            'green': green_cost,
            'white': white_cost,
            'colorless': colorless_cost,
            'generic': generic_cost,
            'life': life_cost,
            'discard': discard_cost,
            'loyalty': loyalty_cost,
            'sacrifice': sacrifice_cost,
            'hybrid': hybrid_cost,
            'tap': tap_cost,
            'untap': untap_cost,
        }

    @staticmethod
    def get_normalized_effect(raw_effect_string):
        # TODO: see test for normalized effect format
        normalized_effect_tokens = OracleTextParser.get_normalized_tokens(raw_effect_string)
        return OracleTextParser.classify_effect_tokens(normalized_effect_tokens)

    @staticmethod
    def is_token_nounish(token):
        return True if token.pos_ == "NOUN" or \
                       token.pos_ == "-PRON-" or \
                        token.pos_ == "PROPN" \
            else False

    @staticmethod
    def is_token_interesting(token):
        DEBUG("checking if token is interesting: " + token.text + " " + str(token.pos_))
        return True if OracleTextParser.is_token_nounish(token) or \
                token.pos_.count('ADJ') or \
                token.pos_.count('VERB') or \
                token.pos_.count('ADV') or \
                token.pos_.count('ADP') \
            else False

    @staticmethod
    def classify_effect_tokens(effect_tokens):
        DEBUG('classifying effect tokens')
        # build bigrams
        bigrams = []
        for first_token_index in range(len(effect_tokens)):
            first_token = effect_tokens[first_token_index]
            if OracleTextParser.is_token_interesting(first_token):
                bigram = first_token.text
                for second_token_index in range(first_token_index + 1, len(effect_tokens)):
                    second_token = effect_tokens[second_token_index]
                    if OracleTextParser.is_token_interesting(second_token):
                        bigram += ' ' + second_token.text
                        bigrams.append(bigram)
                        break

        return {
            'bigrams': bigrams,
            'effect': effect_tokens,
            'tokens': [w.text for w in effect_tokens],
            'nouns': [w.text for w in effect_tokens if OracleTextParser.is_token_nounish(w)],
            'verbs': [w.text for w in effect_tokens if w.pos_ == "VERB"],
            'phrases': [phrase.text for phrase in effect_tokens.noun_chunks],
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
