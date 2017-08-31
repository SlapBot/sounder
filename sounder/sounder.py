# noinspection PyPep8Naming
import sys
from munkres import Munkres
from difflib import SequenceMatcher as sm
from metaphone import doublemetaphone as dm


# noinspection PyShadowingNames
class Sounder:
    def __init__(self, dataset=[]):
        self.dataset = dataset
        self.reserved_sub_words = self.get_reserved_sub_words()

    def set_dataset(self, dataset):
        self.dataset = dataset
        return self

    def set_filter(self, reserved_sub_words):
        self.reserved_sub_words = reserved_sub_words

    def get_metaphones(self, query, dataset):
        new_query = [dm(given_keyword)[0] for given_keyword in query]
        new_dataset = []
        for data in dataset:
            user_keywords = [dm(user_keyword)[0] for user_keyword in data]
            new_dataset.append(user_keywords)
        return new_query, new_dataset

    @staticmethod
    def get_reserved_sub_words():
        return {
            "what", "where", "which", "how", "when", "who",
            "is", "are", "makes", "made", "make", "did", "do",
            "to", "the", "of", "from", "against", "and", "or",
            "you", "me", "we", "us", "your", "my", "mine", 'yours',
            "could", "would", "may", "might", "let", "possibly",
            'tell', "give", "told", "gave", "know", "knew",
            'a', 'am', 'an', 'i', 'like', 'has', 'have', 'need',
            'will', 'be', "this", 'that', "for"
        }

    def filter(self, query, reserved_sub_words=None):
        if reserved_sub_words:
            self.reserved_sub_words = reserved_sub_words
        sub_words = []
        reserved_sub_words = self.get_reserved_sub_words()
        raw_text_array = query.lower().split()
        key_words = raw_text_array.copy()
        for index, raw_text in enumerate(raw_text_array):
            if raw_text in self.reserved_sub_words:
                sub_words.append(raw_text)
                key_words.remove(raw_text)
        return { 'sub_words': sub_words, 'key_words': key_words}

    def search(self, query, dataset=None, metaphone=False):
        if dataset:
            self.dataset = dataset
        if self.dataset:
            if metaphone:
                query, self.dataset = self.get_metaphones(query, dataset)
            index = self.process(self.dataset, query)
        else:
            raise TypeError("Missing dataset parameter since it's not been initialized either.")
        return index

    def probability(self, query, dataset=None, detailed=False, prediction=False, metaphone=False):
        if dataset:
            if any(isinstance(i, str) for i in dataset):
                dataset = [dataset]
            self.dataset = dataset
        if self.dataset:
            if metaphone:
                query, self.dataset = self.get_metaphones(query, self.dataset)
            chances = self.process_chances(self.dataset, query)
        else:
            raise TypeError("Missing dataset parameter since it's not been initialized either.")
        if prediction:
            index = self.pick(chances)
            if detailed:
                return {
                'chances': chances[index],
                'index': index
                }
            return {
                'chances': chances[index][0],
                'index': index
                }
        if detailed:
            return chances
        return [chance[0] for chance in chances]

    def process_chances(self, dataset, query):
        scores = []
        for data in dataset:
            temp_scores = self.process_words(data, query)
            word_score = self.pick_most_probable_word(temp_scores, len(data))
            avg_score = sum(word_score) / len(word_score)
            scores.append([avg_score, word_score])
        return scores

    def process(self, dataset, query):
        scores = []
        for data in dataset:
            temp_scores = self.process_words(data, query)
            word_score = self.pick_most_probable_word(temp_scores, len(data))
            avg_score = sum(word_score) / len(word_score)
            scores.append([avg_score, word_score])
        return self.pick(scores)

    def process_words(self, data, query):
        temp_scores = []
        avg_scores_list = []
        for index, s_word in enumerate(data):
            avg_scores = [0 for _ in range(0, len(query))]
            for index, k_word in enumerate(query):
                avg_scores[index] = self.loop2(k_word, s_word)
            avg_scores_list.append(avg_scores)
        temp_scores = self.hungarian_algorithm(avg_scores_list)
        return temp_scores

    @staticmethod
    def pick_most_probable_word(temp_scores, length):
        word_score = [0 for _ in range(0, length)]
        for index, temp_score in enumerate(temp_scores):
            word_score[index] = temp_score[0]
        return word_score

    @staticmethod
    def hungarian_algorithm(matrix):
        temp_scores = []
        cost_matrix = []
        for row in matrix:
            cost_row = []
            for col in row:
                cost_row += [sys.maxsize - col]
            cost_matrix += [cost_row]
        m = Munkres()
        indexes = m.compute(cost_matrix)
        for row, column in indexes:
            score = matrix[row][column]
            index = column
            temp_scores.append([score, index])
        return temp_scores

    @staticmethod
    def loop2(k_word, s_word):
        word_score = sm(None, k_word, s_word)
        return round(word_score.ratio() * 100)

    @staticmethod
    def pick(scores):
        max_score = 0
        max_index = 0
        for index, item in enumerate(scores):
            if item[0] > max_score:
                max_score = item[0]
                max_index = index
        picked = scores[max_index][1]
        perm_sum = sum(picked)
        perm_avg = perm_sum / len(picked)
        for index, item in enumerate(scores):
            if item[0] == max_score and index != max_index:
                temp_sum = sum(item[1])
                temp_avg = temp_sum / len(item[1])
                if temp_avg > perm_avg:
                    max_index = index
                    perm_sum = temp_sum
                    perm_avg = temp_avg
                elif temp_avg == perm_avg:
                    if temp_sum > perm_sum:
                        max_index = index
                        perm_sum = temp_sum
                        perm_avg = temp_avg
        return max_index
