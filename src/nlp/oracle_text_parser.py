class OracleTextParser:
    @staticmethod
    def get_cost_and_effect_from_action(action):
        cost_effect_parts = action.split(':')
        print(str(cost_effect_parts[0]))
        return cost_effect_parts[0].strip(' '), ':'.join(cost_effect_parts[1:]).strip(' ')

    @staticmethod
    def get_normalized_tokens(raw_string):
        return raw_string.split(' ')

    @staticmethod
    def get_action_list_from_raw_card_text(raw_card_text):
        return [action.strip(' ') for action in raw_card_text.split("\n")]

    @staticmethod
    def get_normalized_cost_tokens(raw_cost_string):
        normalized_cost_tokens = OracleTextParser.get_normalized_tokens(raw_cost_string)
        return OracleTextParser.classify_cost_tokens(normalized_cost_tokens)

    @staticmethod
    def classify_cost_tokens(cost_tokens):
        return {
            'tokens': cost_tokens,
            'nouns': [],
            'verbs': [],
            'phrases': [],
            '1-grams': [],
            '2-grams': [],
            '3-grams': []
        }

    @staticmethod
    def get_normalized_effect(raw_effect_string):
        # TODO: see test for normalized effect format
        normalized_effect_tokens = OracleTextParser.get_normalized_tokens(raw_effect_string)
        return OracleTextParser.classify_effect_tokens(normalized_effect_tokens)

    @staticmethod
    def classify_effect_tokens(effect_tokens):
        return {
            'tokens': effect_tokens,
            'nouns': [],
            'verbs': [],
            'phrases': [],
            '1-grams': [],
            '2-grams': [],
            '3-grams': []
        }

    @staticmethod
    def classify_cost_tokens(cost_tokens):
        return OracleTextParser.classify_tokens(cost_tokens)

    @staticmethod
    def classify_action_tokens(action_tokens):
        return OracleTextParser.classify_tokens(action_tokens)

    @staticmethod
    def basic_card_text_parser(raw_card_text):
        # test_preprocessed_card_text_is_separated_into_actions
        action_list = OracleTextParser.get_action_list_from_raw_card_text(raw_card_text)
        results = []
        for action in action_list:
            # preprocessed_card_text_is_separated_into_actions_and_casting_costs:
            cost_action_tuple = OracleTextParser.get_cost_and_effect_from_action(action)
            cost = cost_action_tuple[0]
            action = cost_action_tuple[1]

            # preprocessed_card_text_is_tokenized():
            cost_token_list = OracleTextParser.get_normalized_cost_tokens(cost)
            actions_token_list = OracleTextParser.get_normalized_action_tokens(action)

            # preprocessed_card_text_is_classified():
            classified_cost_tokens = OracleTextParser.classify_cost_tokens(cost_token_list)
            classified_action_tokens = OracleTextParser.classify_action_tokens(actions_token_list)
            results.append({
                'cost_tokens': classified_cost_tokens,
                'action_tokens': classified_action_tokens
            })
        return results

