"""
core.py
"""

import string
from collections import defaultdict
import multiprocessing as mp
import numpy as np
import pandas as pd
from nltk import word_tokenize

TRANSLATE_TABLE = dict((ord(char), None) for char in string.punctuation)


class LIWC():
    """Top-level class"""

    def __init__(self, dict_path):
        self.lexicon, self.category_names = self._read_dic(dict_path)
        self.trie = self._build_trie(self.lexicon)

    def process_text(self, text):
        """Run LIWC on string"""

        tokenized = word_tokenize(text.lower().translate(TRANSLATE_TABLE))
        counts = defaultdict(int)
        dict_count = len(tokenized)

        for token in tokenized:
            classifications = list(self._parse_token(token))

            if not classifications:
                dict_count -= 1
            else:
                for category in classifications:
                    counts[category] += 1

        category_scores = {category: (
            counts[category] / len(tokenized)) * 100 for category in counts.keys()}

        return category_scores

    def process_df_mp(self, df, col):
        """Multi-process version of process_df"""
        cpu_count = mp.cpu_count()
        p = mp.Pool(cpu_count)

        batches = np.array_split(df, cpu_count)

        pool_results = p.starmap(self.process_df,[(batch, col) for batch in batches if len(batch) > 0])
        p.close()
        
        return pd.concat(pool_results, axis=0)

    def process_df(self, df, col):
        """Run LIWC on a dataframe column"""
        df[col] = df[col].astype(str)

        def apply_df(row, col):
            score = self.process_text(row[col])
            scores = {}
            
            for category in score:
                scores[category] = score[category]

            return pd.Series(scores)


        res = df.apply(apply_df, args=(col,), axis=1)

        return res


    def _read_dic(self, filepath):
        category_mapping = {}
        category_names = []
        lexicon = {}
        mode = 0    # the mode is incremented by each '%' line in the file
        with open(filepath) as dict_file:
            for line in dict_file:
                tsv = line.strip()
                if tsv:
                    parts = tsv.split('\t')
                    if parts[0] == '%':
                        mode += 1
                    elif mode == 1:
                        # definining categories
                        category_names.append(parts[1])
                        category_mapping[parts[0]] = parts[1]
                    elif mode == 2:
                        lexicon[parts[0]] = [category_mapping[category_id]
                                             for category_id in parts[1:]]
        return lexicon, category_names

    def _build_trie(self, lexicon):
        '''
        Build a character-trie from the plain pattern_string -> categories_list
        mapping provided by `lexicon`.

        Some LIWC patterns end with a `*` to indicate a wildcard match.
        '''
        trie = {}
        for pattern, category_names in lexicon.items():
            cursor = trie
            for char in pattern:
                if char == '*':
                    cursor['*'] = category_names
                    break
                if char not in cursor:
                    cursor[char] = {}
                cursor = cursor[char]
            cursor['$'] = category_names
        return trie

    def _search_trie(self, trie, token, token_i=0):
        '''
        Search the given character-trie for paths that match the `token` string.
        '''
        if '*' in trie:
            return trie['*']
        elif '$' in trie and token_i == len(token):
            return trie['$']
        elif token_i < len(token):
            char = token[token_i]
            if char in trie:
                return self._search_trie(trie[char], token, token_i + 1)
        return []

    def _parse_token(self, token):
        for category_name in self._search_trie(self.trie, token):
            yield category_name
