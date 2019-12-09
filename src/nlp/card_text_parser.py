class CardTextParser:
    def __init__(self):
        return

    def get_action_list_from_raw_card_text(self, raw_card_text):
        return [action.strip(' ') for action in raw_card_text.split("\n")]

    def get_cost_and_description_from_action(self, action):
        cost_action_parts = action.split(':')
        return (cost_action_parts[0], cost_action_parts[1:])

    def get_normalized_tokens(self, raw_string):
        return raw_string.split(' ')

    def get_normalized_cost_tokens(self, raw_cost_string):
        return self.get_normalized_tokens(raw_cost_string)

    def get_normalized_action_tokens(self, raw_action_string):
        return self.get_normalized_tokens(raw_action_string)

    def classify_tokens(self, tokens):
        return {
            'tokens': tokens,
            'nouns': [],
            'verbs': [],
            'phrases': [],
            '1-grams': [],
            '2-grams': [],
            '3-grams': []
        }

    def classify_cost_tokens(self, cost_tokens):
        return self.classify_tokens(cost_tokens)

    def classify_action_tokens(self, action_tokens):
        return self.classify_tokens(action_tokens)

    def basic_card_text_parser(self, raw_card_text):
        # test_preprocessed_card_text_is_separated_into_actions
        action_list = self.get_action_list_from_raw_card_text(raw_card_text)
        results = []
        for action in action_list:
            # preprocessed_card_text_is_separated_into_actions_and_casting_costs:
            cost_action_tuple = self.get_cost_and_description_from_action(action)
            cost = cost_action_tuple[0]
            action = cost_action_tuple[1]

            # preprocessed_card_text_is_tokenized():
            cost_token_list = self.get_normalized_cost_tokens(cost)
            actions_token_list = self.get_normalized_action_tokens(action)

            # preprocessed_card_text_is_classified():
            classified_cost_tokens = self.classify_cost_tokens(cost_token_list)
            classified_action_tokens = self.classify_action_tokens(actions_token_list)
            results.append({
                'cost_tokens': classified_cost_tokens,
                'action_tokens': classified_action_tokens
            })
        return results

