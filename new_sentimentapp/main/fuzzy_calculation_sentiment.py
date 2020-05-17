class FuzzySentiment:
    FUZZY_RULES = {
        ('subj_low', 'polarity_low', 'emoji_low'): 'low',
        ('subj_low', 'polarity_low', 'emoji_medium'): 'low',
        ('subj_low', 'polarity_low', 'emoji_high'): 'medium',
        ('subj_low', 'polarity_medium', 'emoji_low'): 'low',
        ('subj_low', 'polarity_medium', 'emoji_medium'): 'medium',
        ('subj_low', 'polarity_medium', 'emoji_high'): 'high',
        ('subj_low', 'polarity_high', 'emoji_low'): 'medium',
        ('subj_low', 'polarity_high', 'emoji_medium'): 'high',
        ('subj_low', 'polarity_high', 'emoji_high'): 'high',
        ('subj_high', 'polarity_low', 'emoji_low'): 'low',
        ('subj_high', 'polarity_low', 'emoji_medium'): 'low',
        ('subj_high', 'polarity_low', 'emoji_high'): 'low',
        ('subj_high', 'polarity_medium', 'emoji_low'): 'low',
        ('subj_high', 'polarity_medium', 'emoji_medium'): 'medium',
        ('subj_high', 'polarity_medium', 'emoji_high'): 'high',
        ('subj_high', 'polarity_high', 'emoji_low'): 'medium',
        ('subj_high', 'polarity_high', 'emoji_medium'): 'high',
        ('subj_high', 'polarity_high', 'emoji_high'): 'high',
        ('subj_medium', 'polarity_low', 'emoji_low'): 'low',
        ('subj_medium', 'polarity_low', 'emoji_medium'): 'low',
        ('subj_medium', 'polarity_low', 'emoji_high'): 'low',
        ('subj_medium', 'polarity_medium', 'emoji_low'): 'low',
        ('subj_medium', 'polarity_medium', 'emoji_medium'): 'medium',
        ('subj_medium', 'polarity_medium', 'emoji_high'): 'high',
        ('subj_medium', 'polarity_high', 'emoji_low'): 'medium',
        ('subj_medium', 'polarity_high', 'emoji_medium'): 'high',
        ('subj_medium', 'polarity_high', 'emoji_high'): 'high'
    }

    def __init__(self):
        self.a = 20
        self.b = 40
        self.c = 60
        self.d = 80
        self.center_of_gravity_low = (self.a + 0) / 2
        self.center_of_gravity_medium = (self.b + self.c) / 2
        self.center_of_gravity_high = (self.d + 100) / 2

    def low_graph(self, x):
        if x > self.b:
            return 0
        if self.a <= x <= self.b:
            return (self.b - x) / (self.b - self.a)
        if x < self.a:
            return 1

    def medium_graph(self, x):
        if x <= self.a or x >= self.d:
            return 0
        if self.a <= x < self.b:
            return (x - self.a) / (self.b - self.a)
        if self.b <= x < self.c:
            return 1
        if self.c <= x < self.d:
            return (self.d - x) / (self.d - self.c)

    def high_graph(self, x):
        if x <= self.c:
            return 0
        if self.c < x < self.d:
            return (x - self.c) / (self.d - self.c)
        if x >= self.d:
            return 1

    def get_membership(self, value, fuzzy_set):
        func_full_name = '{}_graph'.format(fuzzy_set)
        return getattr(self, func_full_name)(value)

    def get_weight_of_rules(self, subj, pol, emoj):
        crisp_values = [subj, pol, emoj]
        rules_weights = []
        for i in self.FUZZY_RULES:
            values = []
            for j in range(3):
                fuzzy_set_name = i[j].split('_')[1]
                values.append(self.get_membership(crisp_values[j], fuzzy_set_name))
            rules_weights.append((min(values), self.FUZZY_RULES[i]))
        return rules_weights

    def defuzzification_singleton(self, rules_weights):
        avg = 0
        for i in rules_weights:
            avg += (i[0] * getattr(self, 'center_of_gravity_{}'.format(i[1])))
        weight_sum = sum([k[0] for k in rules_weights])
        if weight_sum != 0:
            return avg / sum([k[0] for k in rules_weights])

    def get_sentiment(self, subj_value, polarity_value, emoji_value):
        weighted_rules = self.get_weight_of_rules(subj_value, polarity_value, emoji_value)
        final_value = self.defuzzification_singleton(weighted_rules)
        print(final_value)
        output_sets = set(self.FUZZY_RULES.values())
        max_sentiment = {}
        for o_set in output_sets:
            max_sentiment[o_set] = getattr(self, '{}_graph'.format(o_set))(final_value)
        return max(max_sentiment.items(), key=lambda x: x[1])[0]

fs=FuzzySentiment()

